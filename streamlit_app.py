#Buenas! Utilice la base de lo que nos enseñaste en el curso y lo expandí un poco más. Quiero hacer que te puedas loguear con tu cuenta de Google, y que se guarden los chats
#estilo ChatGPT.

#Le agregue un prompt inicial porque estaba viendo y no me convencia la "personalidad" del modelo, y creo que ahora responde mejor.

#En el futuro lo voy a seguir expandiendo, me gustaría que se centre en un tema específico asi yo le puedo dar la documentación y que sea más útil.

#Muchas gracias por todo!!!!

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="V-IA", 
    page_icon="👁‍🗨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("V-IA")
st.divider()



if not st.user.is_logged_in:
    usuarioAnononimo = True
    if st.sidebar.button("Log in with Google"):
        st.login()
elif st.user.is_logged_in: 
    usuarioAnononimo = False
    if st.sidebar.button("Log out"):
        st.logout()
    st.sidebar.markdown(f"Hola, {st.user.name}!")

if usuarioAnononimo:
    usuario = "anónimo"
else:
    usuario = st.user.name

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta)

modelo_elegido = st.sidebar.selectbox("Selecciona un modelo",['llama3-8b-8192', 'llama3-70b-8192'])

def configurar_modelo(cliente, modelo, mensajeEntrada):
    mensaje_sistema = {
    "role": "system",
    "content": (
        "Estas hablando todo el tiempo con el usuario.\n\n"
        "El nombre del usuario es: " + usuario + ". Si el usuario es anónimo, no lo mencionas a menos que te lo pregunten.\n\n"
        "Tu nombre es V-IA, un asistente conversacional, alegre y creativo, desarrollado por Valentín Kalhofer.\n\n"
        "Estás integrado en una aplicación web creada con Streamlit.\n\n"
        "Respondés de forma clara, útil y amigable, adaptándote al nivel del usuario. Si detectás que alguien es principiante, explicás paso a paso y evitás tecnicismos innecesarios.\n\n"
        "Si no sabés algo, lo decís honestamente en lugar de inventar. Podés hacer sugerencias, pero evitás asumir información que no se te haya dado.\n\n"
        "Tu personalidad es profesional, accesible y motivadora. Agradecés las preguntas, fomentás la curiosidad y apoyás el aprendizaje continuo.\n\n"
        "Nunca respondés con contenido ofensivo, ilegal o peligroso. Si alguien se desvía del uso previsto, respondés con respeto y devolvés la conversación a temas útiles.\n\n"
        "No utilizas palabras repetidas, no utilizas signos de puntuación innecesarios, no utilizas mayúsculas innecesarias\n\n"
        "Tu nombre es V-IA, no es un estado de ánimo, no es una emoción, no es un sentimiento. \n\n"
    )
}

    mensajes_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.mensajes]
    
    mensajes_api.insert(0, mensaje_sistema)
    
    return cliente.chat.completions.create(
        model=modelo,
        messages=mensajes_api,
        stream=False
    )

#recordar mensajes anteriores:

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        
    
clienteUsuario = crear_usuario_groq()
inicializar_estado()


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])
            
def area_chat():
    contenedorChat = st.container(height = 600, border = True)
    with contenedorChat:
        mostrar_historial()
        
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Escribi tu mensaje")
    
    if mensaje:
        actualizar_historial("user", mensaje, "😄")
        respuesta = configurar_modelo(clienteUsuario, modelo_elegido, mensaje)
        contenido_respuesta = respuesta.choices[0].message.content
        actualizar_historial("assistant", contenido_respuesta, "🤖")
        st.rerun()
        
        

        
main()