Playfair cypher

LINUX:

rodar o programa no terminal:

# python3 main.py


WINDOWS:

duplo clique sobre main.py

caso esteja usando o wsl, tambem é preciso instalar um Xserver
no windows por exemplo Xming, que pode ser baixado na seguinte
pagina:

https://sourceforge.net/projects/xming/


uma vez com o Xserver instalado e rodando você deve instalar
aplicações gráficas com o seguinte comando:

# sudo apt-get install x11-apps


agora é só setar o display com o comando:

# export DISPLAY=:0


e rodar o programa:

# python3 main.py