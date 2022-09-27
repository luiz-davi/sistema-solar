import sys
import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# Variaveis globais
global angulo, fAspect, rotX, rotY, rotZ, obsX, obsY, obsZ, solAtivo
global rotX_ini, rotY_ini, obsX_ini, obsY_ini, obsZ_ini, x_ini, y_ini, botao
global sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune

solAtivo = True
orbita = True
eixoX, eixoY, eixoZ = 0, 0, 0

# Constantes utilizadas na interacao com o mouse
SENS_ROT = 5.0
SENS_OBS = 10.0
SENS_TRANSL = 10.0

# Modela o objeto esferico, rotaciona e translada
def Desenha_planeta(textura, pos_y, pos_x, escala, diametro, raio):
  t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
  a = t*2
  # GLUT_ELAPSED_TIME eh o numero de segundos desde que glutInit foi chamado

  # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
  # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
  glPushMatrix()
  glTranslated(0, -pos_y, 0) # produz a matriz de translacao especificada por (x, y, z)
  
  # Movimento de Translacao - transf. geometrica que move todas as coordenadas dos objetos ao longo dos eixos coordenados
  glTranslatef((pos_x * math.cos(2.0 * 3.14 * a*raio / 100)),(pos_y +pos_y * math.sin(2.0 * 3.14 * a*raio/ 100)), 0)
  obj = gluNewQuadric() # Estrutura de dado para modelar uma quadrica (esfera, cone, cilindro, disco...)
  gluQuadricTexture(obj, GL_TRUE) # Especifica que o objeto deve ser texturizado
  glEnable(GL_TEXTURE_2D)  # Habilita o recurso da textura para poder alterar
  glBindTexture(GL_TEXTURE_2D, textura) # Cria uma textura nomeada, para usar no programa 
  glScalef(escala,escala, escala) # altera a escala do objeto ao longo dos eixos
  glRotated(a * 20, 0, 0, 1) # calcula uma matriz que executa uma rotacao
  gluSphere(obj, diametro, 25, 25)  # desenha uma esfera
  glDisable(GL_TEXTURE_2D) # Desabilita alteracoes em textura
  glPopMatrix() # Fim do push

def Desenha_planetas_com_Satelites_e_Aneis(textura_planeta, textura_satelite, textura_aneis, pos_y, pos_x, escala, diametro1, diametro2, raio, raio_lua):

  tempo = glutGet(GLUT_ELAPSED_TIME) / 1000.0
  angulo = tempo * 2

  # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
  # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
  glPushMatrix()
  # glutBitmapString(GLUT_BITMAP_9_BY_15, planeta)
  glTranslated(0, -pos_y, 0)
  # Movimento de Translacao
  glTranslatef((pos_x * math.cos(2.0 * 3.14 * angulo * raio / 100)),(pos_y +pos_y * math.sin(2.0 * 3.14 * angulo * raio/ 100)), 0)
  obj = gluNewQuadric()
  gluQuadricTexture(obj, GL_TRUE)
  glEnable(GL_TEXTURE_2D)
  glBindTexture(GL_TEXTURE_2D,textura_planeta)
  glScalef(escala,escala,escala)
  glRotated(angulo * 20, 0, 0, 1)
  gluSphere(obj,diametro1,25,25)
  glScalef(escala,escala,escala)
  # Desenha o anel
  glEnable(GL_TEXTURE_2D)
  glBindTexture(GL_TEXTURE_2D, textura_aneis)
  desenhaAnel(pos_x/80,pos_y/80)

  # Satelite
  # Translacao da Lua
  glTranslatef(pos_x/20*(math.cos(2.0 * 3.14 * angulo * raio_lua / 100)),(pos_y/20*math.sin(2.0 * 3.14 * angulo * raio_lua / 100)), 0)
  glBindTexture(GL_TEXTURE_2D,textura_satelite)
  glScalef(escala,escala,escala)
  glRotated(angulo * 5, 1, 0, 1)
  gluSphere(obj,diametro2,50,50)
  glDisable(GL_TEXTURE_2D)

  glPopMatrix() # Fim do push

def desenha_planetas_com_Satelites(textura_planeta, textura_satelite, pos_y, pos_x, escala, diametro1, diametro2, raio, raio_lua):
  tempo = glutGet(GLUT_ELAPSED_TIME) / 1000.0 # Tempo desde que o glutInit foi chamado
  angulo = tempo * 2 

  # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
  # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
  glPushMatrix()
  # Produz uma matriz de translação em x,y,z
  glTranslated(0, -pos_y, 0)
  # Movimento de Translacao
  glTranslatef((pos_x * math.cos(2.0 * 3.14 * angulo * raio / 100)),(pos_y + pos_y * math.sin(2.0 * 3.14 * angulo * raio / 100)), 0)
  obj = gluNewQuadric() # Cria a quadrica
  gluQuadricTexture(obj, GL_TRUE) # Especifica textura na quadrica
  glEnable(GL_TEXTURE_2D) # Habilita a textura
  glBindTexture(GL_TEXTURE_2D, textura_planeta) # Define o nome da textura do planeta
  glScalef(escala, escala, escala) # Define o tamanho do objeto
  glRotated(angulo * 20, 0, 0, 1) # Define a matriz de rotação em torno de si mesmo
  gluSphere(obj, diametro1, 25, 25) # Cria a esfera a partir da quadrica e do diametro, uniformidade do objeto é definido pelos últimos dois parametros

  # Satelite
  # Translacao da Lua
  glTranslatef(pos_x/10*(math.cos(2.0 * 3.14 * angulo * raio_lua / 100)),(pos_y/10*math.sin(2.0 * 3.14 * angulo * raio_lua / 100)), 0)

  glBindTexture(GL_TEXTURE_2D,textura_satelite) # Coloca a textura na lua
  glScalef(escala,escala,escala) # Define a escala da lua
  glRotated(angulo * 5, 1, 0, 1) # Define a rotação da lua
  gluSphere(obj,diametro2,50,50) # Desenha a esfera da lua
  glDisable(GL_TEXTURE_2D) # Conclui o desenho

  glPopMatrix() # Fim do push

def desenhaAnel(eixoX, eixoY):
  # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
  # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
  glPushMatrix()
  # glBegin Inicia uma lista de vertices, e o argumento determina qual objeto sera desenhado
  # GL_LINE_LOOP exibe uma sequencia de linhas conectando os pontos definidos por glVertex e ao final liga o primeiro como ultimo ponto
  glBegin(GL_LINE_LOOP)
  for i in range(360):
    rad = i*3.14/180
    glVertex2f(math.cos(rad)*eixoX,math.sin(rad)*eixoY) # Especifica um vertice
  glEnd() # Fim do begin
  # Retira a matriz do topo da pilha e torna esta ultima a matriz de transformacao corrente
  glPopMatrix() # Fim do push

def Desenha():
  glDrawBuffer(GL_BACK)
  # Limpa a janela de visualizao com a cor de fundo especificada
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  # desenha todos os objetos na tela
  Sistema_Solar()
  glutSwapBuffers()

# Desenha o sistema solar e as orbitas dos planetas
def Sistema_Solar():
  global mercury, venus

  tempo = glutGet(GLUT_ELAPSED_TIME) / 1000.0 # Tempo desde que o GlutInit foi inicializado
  angulo = tempo
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  # SOL
  if(solAtivo):
    # Desabilita a iluminação, glColor que definimos nas orbitas por exemplo será visível
    glDisable(GL_LIGHTING) 
    glDisable(GL_LIGHT0)

    glPushMatrix()
    qobj = gluNewQuadric() # Gera a quádrica para definir o objeto
    gluQuadricTexture(qobj, GL_TRUE) # Indica que quádrica vai ter textura aplicada
    glEnable(GL_TEXTURE_2D) # Habilita a textura
    glBindTexture(GL_TEXTURE_2D,sun) # Especifica a textura do Sol na quádrica
    glRotated(angulo * 7, 0, 0, 1) # Rotaciona o objeto para formato o movimento de rotação do Sol em torno de si mesmo
    glScalef(3,3,3) # Aumenta o tamanho (escala) do Sol
    gluSphere(qobj,1,50,50) # Cria a espera do Sol a partir da quádrica
    glPopMatrix() # Fim do push
    glDisable(GL_TEXTURE_2D)
  else:
    # Habilita a iluminação, glColor que definimos nas orbitas não será visível
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

   # MERCURIO - Diametro: 4.879,4 km
  Desenha_planeta(mercury, 7, 7, 2,0.48,3.7)

  # VENUS - Diametro: 12.103,6 km
  Desenha_planeta(venus, 17, 17, 1.2, 1.21 ,2.5)

  # TERRA E LUA - Diametro Terra: 12.756,2 km
  desenha_planetas_com_Satelites(earth, moon, 27, 27, 1.2,1.27,0.5,1.9,0.2)

  # MARTE - Diametro: 6.792,4 km
  desenha_planetas_com_Satelites(mars, moon, 41, 41, 1.2,0.68,0.5,1.9,1)

  # JUPITER - Diametro: 142.984 km
  Desenha_planetas_com_Satelites_e_Aneis(jupiter, moon, saturnRing, 80, 80, 1.5,1.43,0.25,1.9,1)

  # SATURNO - Diametro: 120.536 km
  Desenha_planetas_com_Satelites_e_Aneis(saturn, moon, saturnRing, 97, 97, 1.5,1.2,0.25,1.5,1)

  # URANO - Diametro: 51.118 km
  Desenha_planetas_com_Satelites_e_Aneis(uranus, moon, uranusRing, 107, 107, 1.5,0.9,0.25,1.2,1.3)

  # NETUNO - Diametro: 49.528 km
  Desenha_planetas_com_Satelites_e_Aneis(neptune, moon, uranusRing, 127, 127, 1.5,0.8,0.20,1,1)

# Cria uma orbita
def Desenha_Orbita(pos_y, pos_x):
  # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
  # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
  glPushMatrix()
  glTranslated(0, -pos_y, 0) # Produz uma translacao em (x, y, z)
   # glBegin Inicia uma lista de vertices, e o argumento determina qual objeto sera desenhado
  # GL_LINE_LOOP exibe uma sequencia de linhas conectando os pontos definidos por glVertex e ao final liga o primeiro como ultimo ponto
  glBegin(GL_LINE_LOOP)
  for i in range(100): # Desenha a linha da orbita, a variavel i vai juntando cada linha em uma circunferencia
    glVertex2f(
      pos_x * math.cos(2.0 * 3.14 * i / 100),
      pos_y + pos_y * math.sin(2.0 * 3.14 * i / 100)
    ) # Especifica um vertice

  glEnd() # Fim do begin
  glPopMatrix() # Fim do push


# Chama a funcao para criar as orbitas de cada planeta
def mostraOrbitas():

  # MERCURIO - Diametro: 4.879,4 km
  Desenha_Orbita(7,7)

  # VENUS - Diametro: 12.103,6 km
  Desenha_Orbita(17,17)

  # TERRA - Diametro: 12.756,2 km
  Desenha_Orbita(27,27)

  # MARTE -Diametro: 6.792,4 km
  Desenha_Orbita(41,41)

  # JUPITER - Diametro: 142.984 km
  Desenha_Orbita(80,80)

  # SATURNO - Diametro: 120.536 km
  Desenha_Orbita(97,97)

  # URANO -Diametro: 51.118 km
  Desenha_Orbita(107,107)

  # NETUNO - Diametro: 49.528 km
  Desenha_Orbita(127,127)

def Sistema_Solar_com_orbitas():
  glDrawBuffer(GL_BACK)
  # Limpa a janela de visualizao com a cor de fundo especificada
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  # desenha todos os objetos na tela
  Sistema_Solar()
  mostraOrbitas()
  # Alterna os buffers, entre uma janela (tela) e outra, enquanto a outra é renderizada
  glutSwapBuffers()

def atualiza():
  # Marca o plano normal da janela atual como precisando ser reexibido na proxima iteracao do glutMainLoop
  glutPostRedisplay()

def Inicializa ():
  global angulo, rotX, rotY, rotZ, obsX, obsY, obsZ
  global sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune

  # Inicializa a variavel que especifica o angulo da projecao
  # perspectiva
  angulo = 10
  # Inicializa as variaveis usadas para alterar a posicao do
  # observador virtual
  rotX = 0
  rotY = 0
  rotZ = 0
  obsX = obsY = 0
  obsZ = 150

  sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune = load_images()

  # Especificando que as facetas traseiras serao cortadas
  glEnable(GL_CULL_FACE) # Habilita recursos do GL -> cortar as facetas
  glCullFace(GL_BACK) # Nao mostrar faces do lado de dentro

  glEnable(GL_LIGHTING) # Prepara o OpenGL para realizar calculos de iluminacao
  glEnable(GL_LIGHT0)  # Especifica que a fonte de luz tem cor padrao para luz (branco)
  glEnable(GL_DEPTH_TEST) # Atualiza o buffer de profundidade

# Passos padrao da biblioteca
# Especifica a posicao do observador e do alvo
def PosicionaObservador():
  # Especifica o sistema de coordenadas do modelo
  glMatrixMode(GL_MODELVIEW)
  # Inicializa sistema de coordenadas do modelo
  glLoadIdentity()

  # Posiciona e orienta o observador - transformacoes geometricas de translacao e rotacao em (eixoX, eixoY, eixoZ)
  glTranslatef(-obsX*0.5,-obsY*0.5,-obsZ*0.5)
  glRotatef(rotX,1,0,0)
  glRotatef(rotY,0,1,0)
  glRotatef(rotZ,0,0,1)

# Funcao padrao da biblioteca para especificar o volume de visualizacao
def EspecificaParametrosVisualizacao():
  global angulo
  # Especifica sistema de coordenadas de projecao
  glMatrixMode(GL_PROJECTION)
  # Inicializa sistema de coordenadas de projecao
  glLoadIdentity()
  # Especifica a projecao perspectiva(angulo,aspecto,zMin,zMax)
  gluPerspective(angulo,fAspect,0.5,2000)
  # Especifica a posicao do observador e do alvo
  PosicionaObservador()

# Funcao padrao da biblioteca para alterar o tamanho da tela 
def Redimensiona(w, h):
  global fAspect
  # Para previnir uma divisao por zero
  if ( h == 0 ):
    h = 1

  # Especifica as dimensoes da viewport
  glViewport(0, 0, w, h)
  # Calcula a correção de aspecto
  fAspect = w/h
  # Especifica o volume de visualizacao
  EspecificaParametrosVisualizacao()

# Funcoes para interagir com teclado e mouse
def SpecialKeyboard(tecla, eixoX, eixoY):
  global angulo, rotX, rotY
  # Realiza transformacoes geometricas de rotacao (gira o objeto ao redor do vetor eixoX, eixoY, eixoZ)
  
  if tecla == GLUT_KEY_RIGHT:
    glRotatef(rotX, 1, 0, 0)
    rotX += 1

  elif tecla == GLUT_KEY_LEFT:
    glRotatef(rotY, 0, 1, 0)
    rotY += 1

  elif tecla == GLUT_KEY_DOWN:
    if(angulo<=150):
      angulo +=5 #diminui zoom

  elif tecla == GLUT_KEY_UP:
    if(angulo>=10):
      angulo -=5 #aumenta zoom
  EspecificaParametrosVisualizacao() # Modifica a visualizacao do usuario
  glutPostRedisplay() # Marca para exibir novamente o plano da janela atual na proxima iteracao do glutMainLoop

# Verifica se alguma tecla foi pressionada (com excecao das direcionais)
def teclado(tecla, eixoX, eixoY):
  global solAtivo, orbita, obsZ

  if tecla == chr(27): # Esc para sair
    sys.exit()

  elif tecla == b'l' or tecla == b'L': # Remove o Sol e toda a luz do sistema
    solAtivo = not solAtivo
    glutDisplayFunc(Sistema_Solar_com_orbitas) # Exibe na tela o retorno da funcao chamada

  elif tecla == b'c' or tecla == b'C': # Centraliza no Sol - visao superior do sistema
    obsZ = 50

  elif tecla == b'o' or tecla == b'O': # Mostra ou remove as orbitas
    orbita = not orbita

    if(orbita):
      glutDisplayFunc(Sistema_Solar_com_orbitas) # Exibe na tela o retorno da funcao chamada
    else:
      # Mostra o sistema solar sem as orbitas
      glutDisplayFunc(Desenha) # Exibe na tela o retorno da funcao chamada

  # Volta a matriz ao seu estado padrao (exemplo, comecar da origem em vez do estado atual)
  # Visto que algumas transformacoes sao relativas ao estado atual da matriz (ex: rotacao e translacao)
  glLoadIdentity()
  gluLookAt(obsX,obsY,obsZ, 0,0,0, 0,1,0) # Cria uma matriz de visualizacao derivada de um ponto de vista indicando centro da cena e vetor UP
  glutPostRedisplay() # Marca para exibir novamente o plano da janela atual na proxima iteracao do glutMainLoop

# Gerencia os eventos do mouse, se botao foi pressionado ou nao
def GerenciaMouse(button, state, eixoX, eixoY):
  global obsX, obsY, obsZ, rotX, rotY, obsX_ini, obsY_ini, obsZ_ini, rotX_ini, rotY_ini, x_ini, y_ini, botao

  # Se foi pressionado, salva os parametros atuais
  if (state==GLUT_DOWN):
    x_ini = eixoX
    y_ini = eixoY
    obsX_ini = obsX
    obsY_ini = obsY
    obsZ_ini = obsZ
    rotX_ini = rotX
    rotY_ini = rotY
    botao = button
  else:
    botao = -1

def GerenciaMovimento(eixoX, eixoY):
  global x_ini, y_ini, rotX, rotY, obsX, obsY, obsZ

  # Botao esquerdo do mouse
  if(botao==GLUT_LEFT_BUTTON):
    # Calcula diferenças
    deltax = x_ini - eixoX
    deltay = y_ini - eixoY
    # E modifica angulos
    rotY = rotY_ini - deltax/SENS_ROT
    rotX = rotX_ini - deltay/SENS_ROT

  # Botao direito do mouse
  elif(botao==GLUT_RIGHT_BUTTON):
    deltax = x_ini - eixoX
    deltay = y_ini - eixoY
    # Calcula diferença
    deltaz = deltax - deltay
    # E modifica distancia do observador
    obsZ = obsZ_ini + deltaz/SENS_OBS

  PosicionaObservador() # Padrao da funcao, ja que altera a visualizacao (angulo ou distancia)
  glutPostRedisplay() # Marca para exibir novamente o plano da janela atual na proxima iteracao do glutMainLoop

def main():
  # Inicializa a lib glut, com um contexto openGL especificando a versao e em modo de compatibilidade
  # Sera utilizada para criar janelas, ler o teclado e o mouse
  glutInit(sys.argv)
  glutInitContextVersion(1,1) 
  glutInitContextProfile(GLUT_COMPATIBILITY_PROFILE)

  # Inicia uma janela, definindo tamanho e posicao
  glutInitDisplayMode(GLUT_RGB| GLUT_DOUBLE | GLUT_DEPTH) # Define janela com RGB, profundidade de dois buffers (um exibido e outro renderizando para trocar com o atual)
  glutInitWindowSize(1800,1200)
  glutInitWindowPosition(100,100)
  glutCreateWindow("Sistema Solar")

  # Exibe na tela o retorno da funcao chamada
  glutDisplayFunc(Sistema_Solar_com_orbitas)
  # Remodelagem na janela atual
  glutReshapeFunc(Redimensiona)
  # Define o retorno das teclas direcionais, teclado e mouse para a janela atual (callback gerado por evento)
  glutSpecialFunc(SpecialKeyboard)
  glutKeyboardFunc(teclado)
  glutMouseFunc(GerenciaMouse)
  # Quando o mouse se move dentro da janela enquanto um ou mais botoes do mouse sao pressionados
  glutMotionFunc(GerenciaMovimento)

  # Inicializa ambiente (variaveis, texturas, fonte de luz e atualizacao de profundidade)
  Inicializa()

  # Processamento em segundo plano ou animacao continua. Chama metodo de atualizar a janela atual
  glutIdleFunc(atualiza) 
  # Renderiza a janela criada
  glutMainLoop() 
  return 0

main()