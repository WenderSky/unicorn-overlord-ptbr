#!/usr/bin/env python3
# Licença: GNU GPL v2 (usa o cpk.py dos projetos de recomp de saulob).
"""Instalador da tradução PT-BR de Unicorn Overlord (recomp PC do PS4, github.com/hachi23/unicorn_overlord_pc).
Funciona no Windows e no Steam Deck / Linux, só com a biblioteca padrão do Python.

    patcher.py apply  [pasta_do_jogo] [pasta_traducao]   instala ou atualiza a tradução
    patcher.py revert [pasta_do_jogo]                    devolve os arquivos originais
    patcher.py status [pasta_do_jogo]                    informa se a tradução está instalada

pasta_do_jogo pode ser a pasta do port (onde fica o "Unicorn Overlord.exe" ou a AppImage), a pasta data, a
pasta data/game ou um dos .CPK. Sem ela, o patcher procura sozinho.

O que é feito (nada dos dados originais é sobrescrito; tudo é anexado ao fim dos arquivos):
  - Unicorn_TW.CPK e Unicorn_CN.CPK (os textos que o jogo mostra; com o patch de fãs em inglês, é onde fica o
    inglês): os 31 arquivos de texto em português são anexados e o índice (TOC) passa a apontar para eles.
  - UnicornPatch.CPK: as fontes MsgFont_TW, SysFont_TW (e versões B) e Manofa recebem as letras acentuadas
    redesenhadas. O remendo só é aplicado se a fonte do jogo for exatamente a esperada (SHA-1).
O registro de desfazer fica em <CPK>.ptbr.undo; desinstalar corta o que foi anexado e devolve o índice
original, deixando cada CPK byte a byte como era.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import cpk as cpklib

UNDO_SUFFIX = '.ptbr.undo'
UNDO_MAGIC = b'UOPTUND2'
FONT_MAGIC = b'UOFTXP01'
TEXT_CPKS = ('Unicorn_TW.CPK', 'Unicorn_CN.CPK')
PATCH_CPK = 'UnicornPatch.CPK'


# ------------------------------------------------------------------ Registro de desfazer

def undo_path(cpk_path: Path) -> Path:
    return cpk_path.with_name(cpk_path.name + UNDO_SUFFIX)


def write_undo(path: Path, rec: dict):
    path.write_bytes(UNDO_MAGIC
                     + struct.pack('<QQI', rec['original_len'], rec['header_pos'], len(rec['header'])) + rec['header']
                     + struct.pack('<QI', rec['toc_pos'], len(rec['toc'])) + rec['toc'])


def read_undo(path: Path) -> dict:
    b = path.read_bytes()
    if b[:8] != UNDO_MAGIC:
        raise ValueError(f'{path.name}: registro de desfazer inválido')
    original_len, header_pos, hl = struct.unpack_from('<QQI', b, 8)
    o = 28
    header = b[o:o + hl]; o += hl
    toc_pos, tl = struct.unpack_from('<QI', b, o); o += 12
    return dict(original_len=original_len, header_pos=header_pos, header=header, toc_pos=toc_pos, toc=b[o:o + tl])


def restore(cpk_file: Path, rec: dict):
    with open(cpk_file, 'r+b') as f:
        f.seek(rec['header_pos']); f.write(rec['header'])
        f.seek(rec['toc_pos']); f.write(rec['toc'])
        f.truncate(rec['original_len'])


def installed(cpk_file: Path):
    """O registro de desfazer, se a tradução estiver aplicada neste CPK (senão None)."""
    u = undo_path(cpk_file)
    if not u.exists():
        return None
    rec = read_undo(u)
    if cpk_file.stat().st_size <= rec['original_len']:
        return None   # o arquivo foi reinstalado ou restaurado por fora: o registro não vale mais
    with open(cpk_file, 'rb') as f:
        f.seek(rec['toc_pos'])
        same_place = len(f.read(len(rec['toc']))) == len(rec['toc'])
    return rec if same_place else None


# ------------------------------------------------------------------ Localizar o jogo

def find_file(folder: Path, name: str):
    """Arquivo com esse nome na pasta, sem diferenciar maiúsculas (Unicorn_CN.cpk / .CPK)."""
    if not folder.is_dir():
        return None
    for p in folder.iterdir():
        if p.name.lower() == name.lower() and p.is_file():
            return p
    return None


def game_dir_from(path: Path):
    """data/game a partir de um caminho qualquer dentro da instalação."""
    path = path.expanduser()
    if path.is_file():
        path = path.parent
    for cand in (path, path / 'game', path / 'data' / 'game'):
        if find_file(cand, PATCH_CPK) and find_file(cand, TEXT_CPKS[0]):
            return cand
    return None


def find_game_folder(user_path=None):
    if user_path:
        g = game_dir_from(Path(user_path))
        if g:
            return g
        print(f'Não achei o jogo em: {user_path}')
        return None
    roots = []
    if os.environ.get('VW_DATA_DIR'):
        roots.append(Path(os.environ['VW_DATA_DIR']))
    roots += [SCRIPT_DIR.parent, SCRIPT_DIR.parent.parent, SCRIPT_DIR.parent.parent.parent, Path.cwd(),
              Path.cwd().parent]
    for r in roots:
        g = game_dir_from(r)
        if g:
            return g
    # Pastas comuns de jogos: um ou dois níveis abaixo
    for base in (Path.home() / 'Games', Path.home() / 'games', Path.home() / 'Jogos', Path('/run/media')):
        if not base.is_dir():
            continue
        for depth in ('*', '*/*', '*/*/*'):
            for d in sorted(base.glob(depth)):
                g = game_dir_from(d) if d.is_dir() else None
                if g:
                    return g
    return None


def locate(user_path=None):
    g = find_game_folder(user_path)
    if g is None and not user_path and sys.stdin.isatty():
        typed = input('Não achei o jogo sozinho. Cole o caminho da pasta do jogo (onde está o "Unicorn Overlord.exe" '
                      'ou a AppImage) e aperte Enter:\n> ').strip().strip('"')
        if typed:
            g = find_game_folder(typed)
    if g is None:
        print('Erro: não achei a pasta do jogo (data/game com Unicorn_TW.CPK e UnicornPatch.CPK).\n'
              'Rode de novo informando o caminho, por exemplo:\n'
              '  instalar_traducao_windows.bat "D:\\Jogos\\Unicorn Overlord"')
        return None
    print(f'Jogo encontrado em: {g}')
    return g


# ------------------------------------------------------------------ Aplicar arquivos num CPK

def fms_count(data: bytes):
    return struct.unpack_from('<I', data, 20)[0] if data[:4] == b'FMSB' and len(data) >= 32 else None


def patch_cpk(cpk_file: Path, build) -> bool:
    """build(entry, original_bytes) -> bytes novos ou None. Anexa os novos e repõe o índice."""
    rec = installed(cpk_file)
    if rec:
        print(f'Atualizando a tradução já instalada em {cpk_file.name}...')
        restore(cpk_file, rec)
    arc = cpklib.Cpk(cpk_file)
    try:
        targets = []
        for e in arc.entries:
            new = build(e, arc)
            if new is not None:
                targets.append((e, new))
        if not targets:
            print(f'  {cpk_file.name}: nada a aplicar.')
            return True
        original_toc = arc.toc.packet_bytes()
        rec = dict(original_len=cpk_file.stat().st_size, header_pos=16, header=arc.header.packet_bytes(),
                   toc_pos=arc.toc_offset + 16, toc=original_toc)
        write_undo(undo_path(cpk_file), rec)
        align = arc.align or 0x800
        with open(cpk_file, 'r+b') as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            for e, data in targets:
                pos = (pos + align - 1) // align * align
                f.seek(pos); f.write(data)
                row = e['row']
                arc.toc.set_number(row, 'FileOffset', pos - arc.toc_base)
                arc.toc.set_number(row, 'FileSize', len(data))
                if (row, 'ExtractSize') in arc.toc.positions:
                    arc.toc.set_number(row, 'ExtractSize', len(data))
                pos += len(data)
            new_toc = arc.toc.packet_bytes()
            assert len(new_toc) == len(original_toc), 'o tamanho do TOC mudou'
            f.seek(rec['toc_pos']); f.write(new_toc)
            h = arc.header.rows[0]
            for flag in ('EnableTocCrc', 'EnableFileCrc'):
                if h.get(flag) and (0, flag) in arc.header.positions:
                    arc.header.set_number(0, flag, 0)
            f.seek(rec['header_pos']); f.write(arc.header.packet_bytes())
    finally:
        arc.f.close()
    check = cpklib.Cpk(cpk_file)
    try:
        bad = [e['path'] for e, data in targets if check.read(check.entries[e['row']]) != data]
    finally:
        check.f.close()
    if bad:
        print(f'Erro: a conferência falhou em {cpk_file.name} ({", ".join(bad[:5])}); arquivo devolvido ao original.')
        restore(cpk_file, rec)
        undo_path(cpk_file).unlink()
        return False
    print(f'  {cpk_file.name}: {len(targets)} arquivos aplicados e conferidos.')
    return True


def apply_font_patch(original: bytes, patch: bytes):
    if patch[:8] != FONT_MAGIC:
        raise ValueError('remendo de fonte inválido')
    sha_old, (size, nruns) = patch[8:28], struct.unpack_from('<II', patch, 28)
    if hashlib.sha1(original).digest() != sha_old or len(original) != size:
        return None
    out = bytearray(original)
    o = 36
    for _ in range(nruns):
        off, ln = struct.unpack_from('<II', patch, o); o += 8
        out[off:off + ln] = patch[o:o + ln]; o += ln
    return bytes(out) if hashlib.sha1(out).digest() == patch[o:o + 20] else None


# ------------------------------------------------------------------ Comandos

def apply_translation(game_path, mod_dir):
    g = locate(game_path)
    if not g:
        return False
    mod = Path(mod_dir).resolve() if mod_dir else SCRIPT_DIR.parent / 'arquivos_traducao'
    texts = {('msgsheet/' + p.name).lower(): p.read_bytes() for p in sorted((mod / 'MsgSheet').glob('*.fms'))}
    fonts = {('font_4k/' + p.stem + '.ftx').lower(): p.read_bytes() for p in sorted((mod / 'fontes').glob('*.patch'))}
    if not texts:
        print(f'Erro: não achei os textos em {mod / "MsgSheet"}')
        return False

    ok = True
    skipped = []

    def build_text(e, arc):
        new = texts.get(e['path'].lower())
        if new is None:
            return None
        if fms_count(arc.read(e)) != fms_count(new):
            skipped.append(e['path'])
            return None
        return new

    print('\nAplicando os textos:')
    found = [p for p in (find_file(g, n) for n in TEXT_CPKS) if p]
    for p in found:
        ok &= patch_cpk(p, build_text)
    if skipped:
        print(f'Aviso: {len(set(skipped))} arquivo(s) de texto têm estrutura diferente da esperada e ficaram como '
              f'estavam: {", ".join(sorted(set(skipped)))}')

    fonts_bad = []

    def build_font(e, arc):
        patch = fonts.get(e['path'].lower())
        if patch is None:
            return None
        new = apply_font_patch(arc.read(e), patch)
        if new is None:
            fonts_bad.append(e['path'])
        return new

    print('\nAplicando as fontes (letras acentuadas):')
    ok &= patch_cpk(find_file(g, PATCH_CPK), build_font)
    if fonts_bad:
        print(f'Aviso: {", ".join(fonts_bad)} é diferente da esperada (outra versão do jogo?) e ficou sem as letras '
              f'novas; os acentos podem sair desalinhados.')
    return ok


def revert_translation(game_path):
    g = locate(game_path)
    if not g:
        return False
    any_done = False
    for name in TEXT_CPKS + (PATCH_CPK,):
        p = find_file(g, name)
        if not p:
            continue
        u = undo_path(p)
        rec = installed(p)
        if rec:
            restore(p, rec)
            print(f'  {p.name}: original restaurado.')
            any_done = True
        if u.exists():
            u.unlink()
    print('Tradução removida.' if any_done else 'A tradução não estava instalada.')
    return True


def status(game_path):
    g = locate(game_path)
    if not g:
        return False
    for name in TEXT_CPKS + (PATCH_CPK,):
        p = find_file(g, name)
        if p:
            print(f'  {p.name}: {"tradução instalada" if installed(p) else "original"}')
    return True


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else 'apply'
    rest = [a for a in args[1:] if a]
    if cmd == 'apply':
        ok = apply_translation(rest[0] if rest else None, rest[1] if len(rest) > 1 else None)
    elif cmd == 'revert':
        ok = revert_translation(rest[0] if rest else None)
    elif cmd == 'status':
        ok = status(rest[0] if rest else None)
    else:
        print(__doc__); ok = False
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
