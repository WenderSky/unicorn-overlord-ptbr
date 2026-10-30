# 🦄 Unicorn Overlord (Recomp PC do PS4) — Tradução PT-BR

> Tradução **não-oficial** para **Português do Brasil** de *Unicorn Overlord* na versão de PS4 **recompilada para PC / Steam Deck** ([hachi23/unicorn_overlord_pc](https://github.com/hachi23/unicorn_overlord_pc)).

<p align="center">
  <img alt="Idioma" src="https://img.shields.io/badge/idioma-Portugu%C3%AAs%20(BR)-009c3b">
  <img alt="Plataforma" src="https://img.shields.io/badge/plataforma-PC%20%2B%20Steam%20Deck-1b2838">
  <img alt="Versão" src="https://img.shields.io/badge/vers%C3%A3o-1.0-6a0dad">
  <img alt="Uso" src="https://img.shields.io/badge/uso-n%C3%A3o--comercial-important">
</p>

---

## 📜 Sobre

A tradução para português é do **_Kiri_**, feita para a versão de **Nintendo Switch** (e usada também no PS5). Este pacote **adapta essa tradução para a versão de PS4** que o recomp roda no PC e no Steam Deck.

Não dava para só copiar o arquivo do Switch: o recomp usa a versão asiática do PS4 (com o patch de fãs em inglês), que guarda os textos em outros arquivos e mostra tudo no modo de texto chinês. Nesse modo o jogo não quebra as linhas sozinho e a fonte desenha as letras acentuadas num estilo diferente e desalinhadas. A adaptação resolve isso:

- 📝 Os textos do Switch foram colocados nos arquivos do PS4 (`Unicorn_TW.CPK` / `Unicorn_CN.CPK`), conferindo que cada um tem exatamente a mesma quantidade de falas.
- ↩️ As falas foram **re-quebradas** em linhas de até 50 letras (como o patch em inglês faz), para não saírem das caixas de diálogo.
- 🔤 As letras **á à â ã é ê í ó ô õ ú ç** (e maiúsculas) foram **redesenhadas** nas fontes do jogo, no mesmo estilo e na mesma linha das outras letras.
- 🔘 O botão **"Não"** ganhou o **ã**, que a fonte dos botões não tinha.

> ⚠️ **Aviso:** é uma **tradução de fã**, não oficial, e pode conter erros. Achou algum problema da adaptação (texto saindo da caixa, letra estranha)? Abra uma [*issue*](../../issues). 🙂

### 🎯 Versão do jogo

| Versão | Situação |
|--------|----------|
| 🌏 Ásia — CUSA36381 v1.04, com o patch de fãs em inglês (a que o recomp usa) | ✅ Testada |
| 🌏 Ásia — CUSA36381 sem o patch em inglês | ⚠️ Deve funcionar (o instalador confere cada arquivo), mas não foi testada |

---

## 🎮 O que foi traduzido

**Cerca de 45 mil textos** em 31 arquivos: diálogos da história (quase 26 mil falas), menus, interface, opções, ajuda, missões, classes, habilidades, itens, unidades, arquivos da biblioteca, troféus e falas de batalha.

### 🚫 O que **não** foi traduzido

| Item | Por quê |
|------|---------|
| 14 telas de ajuda com texto desenhado na imagem (ficam em japonês) | A versão traduzida delas está no formato de textura do Switch; fica para uma versão futura |
| Título que abre cada capítulo (aparece como um quadrado) | Problema já existente do patch em inglês no recomp: a fonte grande só tem os ideogramas chineses |
| Créditos finais | Nomes de empresas e pessoas |

---

## 💾 Instalação

> **Requisitos:** o recomp do *Unicorn Overlord* já instalado e funcionando. O instalador usa **Python 3**: no **Steam Deck / Linux** já vem instalado; no **Windows**, se não tiver, baixe em [python.org/downloads](https://www.python.org/downloads/) marcando *"Add python.exe to PATH"*.

### 🪟 Windows

1. Baixe o `.zip` da [última versão](../../releases/latest) e **descompacte** (de preferência dentro da pasta do jogo, a que tem o `Unicorn Overlord.exe`: assim o instalador acha o jogo sozinho).
2. **Feche o jogo.**
3. Dê **duplo-clique** em `instalar_traducao_windows.bat`.
4. Se ele não achar o jogo, cole o caminho da pasta do jogo quando ele pedir (ou arraste a pasta do jogo em cima do `.bat`).
5. Pronto! Abra o jogo. Deixe o **Text Language** em **auto** (o padrão).

### 🎮 Steam Deck / Linux

1. **Feche o jogo** e vá para o **Modo Desktop**.
2. Copie a pasta descompactada para o Deck (de preferência dentro da pasta do jogo, a que tem a AppImage).
3. Abra o **Konsole** nessa pasta e rode:
   ```bash
   chmod +x instalar_traducao_linux.sh
   ./instalar_traducao_linux.sh
   ```
   *(ou `./instalar_traducao_linux.sh "/caminho/da/pasta/do/jogo"`)*

> 💡 Instalou no PC e copiou a pasta do jogo inteira para o Deck? A tradução vai junto, não precisa instalar de novo.

O instalador **não duplica** os arquivos do jogo (o `UnicornPatch.CPK` tem 1 GB): ele anexa os textos e as fontes ao fim dos arquivos e repõe o índice, lendo tudo de volta para conferir. Se algo não bater, ele desfaz sozinho. As fontes só são alteradas se forem exatamente as esperadas.

**Atualizando a tradução?** Rode o instalador da versão nova por cima: ele troca a anterior sem aumentar os arquivos.

---

## ↩️ Como reverter

Dê duplo-clique em `desinstalar_traducao_windows.bat` (ou rode `./desinstalar_traducao_linux.sh`). Os arquivos `Unicorn_TW.CPK`, `Unicorn_CN.CPK` e `UnicornPatch.CPK` voltam **exatamente** ao que eram antes. O índice original fica guardado em `<nome do CPK>.ptbr.undo`, na pasta `data/game` do jogo (não apague esses arquivos).

> Se você mudar o **Text Language** para chinês simplificado, os acentos voltam a ficar desalinhados (só as fontes do modo padrão foram corrigidas).

---

## 🛠️ Como foi feito (resumo técnico)

1. Na versão asiática do PS4, o texto que aparece fica em `Unicorn_TW.CPK` / `Unicorn_CN.CPK` (pacotes **CRI CPK**), com as mensagens em `MsgSheet/*.fms` (formato **FMSB** da Vanillaware). Os 31 arquivos `.fms` da tradução do Switch têm exatamente a mesma estrutura dos do PS4.
2. As linhas longas foram divididas sem tocar nos códigos de controle (`^n/Nome^`, `#c(n)`, `#FN(...)`, `@c(n)`...). Nomes e rótulos de uma linha não foram mexidos.
3. As fontes do modo chinês (`MsgFont_TW`, `SysFont_TW` e versões com brilho, texturas **GNF/BC4**) tinham as letras acentuadas num desenho tipo Times, 11 px abaixo das outras. Cada acentuada foi refeita com a letra sem acento da mesma fonte + o acento (`` ` `` `^` `~`, agudo = grave espelhado) e a cedilha da própria ç. Na **Manofa** (botões), que não tem **ã** na tabela do jogo, o **ä** virou **ã** e o botão usa "Näo".
4. O pacote leva só os blocos da imagem que mudam (220 KB no total), aplicados sobre as fontes do seu próprio jogo depois de conferir o SHA-1.

---

## ⚖️ Licença e uso

Esta é uma **tradução de fã**, feita **sem fins lucrativos** e **sem qualquer afiliação** com a Atlus, a Vanillaware ou a Sega.

- ✅ **Pode** baixar, usar e compartilhar **gratuitamente**.
- ✅ **Pode** repostar, desde que **credite** os autores (_Kiri_ e WenderSky) e **mantenha** este aviso.
- ❌ **É proibido vender, cobrar, monetizar ou lucrar** de qualquer forma com esta tradução.
- ❌ **É proibido distribuir os arquivos do jogo.** Compartilhe **apenas o patch** deste repositório, nunca os `.CPK` ou outros arquivos originais.

*Unicorn Overlord* e todos os nomes relacionados são marcas registradas da **Atlus / Vanillaware / Sega**. Este projeto não é oficial e não substitui a compra do jogo. Veja [LICENSE.txt](LICENSE.txt).

---

## 🙏 Créditos

- **Tradução PT-BR:** **_Kiri_** (versão de Switch / PS5)
- **Adaptação para o PS4 / recomp PC, fontes e instalador:** **WenderSky**
- Recomp para PC: [hachi23/unicorn_overlord_pc](https://github.com/hachi23/unicorn_overlord_pc)

Com a tradução instalada, a tela de título mostra os créditos abaixo de "Pressione qualquer botão".
