import streamlit as st

tutors = [
    {
        "name": "German Andres Gomez",
        # "email": "ger.3.go@gmail.com",
        # "monday": "",
        # "tuesday": "",
        # "wednesday": "",
        # "thursday": "",
        # "friday": "",
        # "saturday": "09:00-17:00",
        # "sunday": "09:00-17:00",
        # "elementary": "MAT, BIO, ING",
        # "middle": "MAT, FIS, BIO, ING",
        # "high": "MAT, FIS, BIO, ING",
        "zone": "2, 3",
        "active": "true",
        "school": "Otro"
    },
    {
        "name": "Santiago Herrera",
        # "email": "santiago@sherpal.co",
        # "monday": "",
        # "tuesday": "",
        # "wednesday": "",
        # "thursday": "",
        # "friday": "",
        # "saturday": "",
        # "sunday": "",
        # "elementary": "BIO, FIS",
        # "middle": "",
        # "high": "BIO",
        "zone": "2",
        "active": "true",
        "school": "Colegio Andino"
    }
]


grades = ["Basico", "Intermedio", "Avanzado"]
grades_mapping = {}

courses = ["Matemáticas", "Biología", "Física", "Español", "Inglés", "Filosofía", "Química", "Francés", "Alemán", "Ciencias Sociales", "Otra"]
course_mapping = {
    "Matemáticas": "MAT",
    "Biología": "BIO",
    "Física": "FIS",
    "Español": "ESP",
    "Inglés": "ING",
    "Filosofía": "FIL",
    "Química": "QUI",
    "Francés": "FRA",
    "Alemán": "ALE",
    "Ciencias Sociales": "CIS",
    "Otra": "OTR",
}

days = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
dyas_mapping = {}

times = ["Mañana", "Tarde", "Noche"]
times_mapping = {}

zones = ["Zona 1", "Zona 2", "Zona 3", "Zona 4", "Zona 5", "Otro"]
zone_mapping = {
    "Zona 1": "1",
    "Zona 2": "2",
    "Zona 3": "3",
    "Zona 4": "4",
    "Zona 5": "5",
    "Otra": "6",
}

schools = [
            'Colegio Andino',
            'Liceo Campo David',
            'Colegio San Carlos',
            'Colegio Nueva Inglaterra',
            'Colegio Reuven Feuerstein',
            'Colegio San Jorge de Inglaterra',
            'Colegio Calatrava',
            'Colegio Colombo Británico',
            'Liceo Navarra',
            'Liceo de Colombia',
            'Colegio Cristiano Monte Hebron',
            'Colegio Los Nogales',
            'Colegio Helvetia',
            'Colegio Marymount',
            'Gimnasio Vermont',
            'Gimnasio Moderno',
            'Gimnasio Campestre',
            'Ginmasio La Montaña',
            'Gi mnasio Nueva Modelia',
            'Colegio The English School',
            'Gimnasio El Hontanar',
            'Colegio Anglo Colombiano',
            'Home School',
            'Otro',
            ]

st.title("Oso de anteojos")
st.text("")
st.text("")

col1, col2, col3 = st.columns(3)

with col1:
    grade = st.multiselect("Nivel educativo", 
                        options=["Todos", *grades],
                        placeholder="Seleccionar",
                        default="Todos",
                        )    
    course = st.multiselect("Curso", 
                        options=["Todos", *courses],
                        placeholder="Seleccionar",
                        default="Todos",
                        )
    
with col2:
    days = st.multiselect("Dias de la semana", 
                        options=["Todos", *days],
                        placeholder="Seleccionar",
                        disabled=True,
                        )
    time = st.multiselect("Hora del dia", 
                        options=["Todos","Mañana", "Tarde", "Noche"], 
                        placeholder="Seleccionar",
                        disabled=True,
                        )

with col3:
    zone = st.multiselect("Zona", 
                        options=["Todos", *zones],
                        placeholder="Seleccionar",
                        default="Todos",
                        )    
    school = st.multiselect("Colegio", 
                        options=["Todos", *schools],
                        placeholder="Seleccionar",
                        default="Todos",
                        )

selected_zones = [zone_mapping[z] for z in zone if z != "Todos"]
selected_courses = [course_mapping[c] for c in course if c != "Todos"]


filtered_tutors = [
    tutor for tutor in tutors
    if (any(z in tutor["zone"] for z in selected_zones) or "Todos" in zone)
    and (tutor["school"] in school or "Todos" in school)
    and (tutor["active"] == "true")
]

if not filtered_tutors:
    st.write("No tutors found with the selected criteria.")
else:
    for tutor in filtered_tutors:
        st.write()    
        st.button(f"{tutor['name']}")