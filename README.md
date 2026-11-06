# Quadra

Basquete de rua em pixel art isométrica, sem dependências nem build: abra `index.html` no navegador. Os sons vêm do `sounds.js`, gerado uma vez pela ElevenLabs; o jogo não usa a chave.

## Como jogar

Você (camisa vermelha) e o parceiro de amarelo enfrentam um adversário por arena. A dupla precisa de 21 pontos; o adversário, de 11. Ao vencer, a dupla avança para a próxima arena; ao perder, pode pedir revanche.

| Arena | Adversário | O que muda |
| --- | --- | --- |
| Quadra da Rua | Rei | Sem poderes |
| Cemitério | Esqueleto | Mais lento, mas rouba e toca a bola de mais longe |
| Base Lunar | Alien | Teletransporte e gravidade baixa para todos |
| Ferro-Velho | Robô | Muito lento, mas arremessa de longe e quase não erra o tempo |
| Inferno | Demônio | Mais rápido, arremessa com fogo e as poças de lava atrasam a dupla |

| Ação | Teclado | Toque |
| --- | --- | --- |
| Mover | Setas ou WASD | Arrastar na tela |
| Arremessar: segure e solte com o marcador no verde | Espaço | Botão vermelho |
| Pular para tocar a bola (na defesa) | Espaço | Botão vermelho |
| Passar, pedir a bola ou roubar | E ou J | Botão azul |
| Pausar | P ou Esc | Botão II |
| Ligar ou desligar o som | M | — |

## Regras

- Dentro da linha de 3 a cesta vale 2; fora dela, 3.
- Quem recupera a bola do adversário precisa limpá-la: levá-la para fora da linha de 3 antes de arremessar. Cesta sem limpar não vale e a posse troca.
- Cada posse tem 16 segundos. Depois de uma cesta, a bola vai para quem sofreu o ponto.
- A marcação próxima piora o arremesso, e o tempo de soltar pesa mais que a distância.

Na tela de título, escolha a arena com ↑ e ↓ e a dificuldade com ← e →.

## Sons

Para gerar um efeito novo, acrescente-o em `scripts/generate_sounds.py`, coloque `ELEVENLABS_API_KEY` no arquivo `.env` (ignorado pelo git) e rode:

```bash
set -a; . ./.env; set +a; python3 scripts/generate_sounds.py
```
