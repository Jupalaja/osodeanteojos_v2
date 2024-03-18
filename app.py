import requests
import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

def map_time_to_period(time_slots):
    periods = {
        "Mañana": (0, 12),   
        "Tarde": (12, 18), 
        "Noche": (18, 24) 
    }

    time_ranges = time_slots.split(", ")
    
    day_periods = set()

    for time_range in time_ranges:
        if not time_range:
            continue
        start_time, end_time = time_range.split("-")
        start_hour = int(start_time.split(":")[0])
        end_hour = int(end_time.split(":")[0])

        for period, (start, end) in periods.items():
            if start_hour < end and end_hour > start:  
                day_periods.add(period)

    return list(day_periods)

def fetch_tutors():
    try:
        response = requests.get("https://mongo-backend-production.up.railway.app/sheets")
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        st.error(f"Ocurrion un error trayendo los tutores: {e}")
        return [] 

def fetch_tutor_username(email):
    try:
        response = requests.get(f"https://mongo-backend-production.up.railway.app/users/search?email={email}")
        response.raise_for_status()  
        tutor = response.json()
        return tutor["username"]
    except requests.RequestException as e:
        st.error(f"Ocurrio un error trayendo el nombre de usuario del tutor: {e}")
        return "ERROR"
    
tutors = fetch_tutors()

zones = ["Zona 1", "Zona 2", "Zona 3", "Zona 4", "Zona 5", "Otra"]
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

available_hours = ["Mañana", "Tarde", "Noche"]

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


st.title("Oso de anteojos")
st.text("")
st.text("")

st.markdown("**Seleccionar Colegio y Zona**")
col1, col2 = st.columns(2)
with col1:
    zone = st.multiselect("Zona", 
                        options=zones,
                        placeholder="Todas",
                        )  
with col2:
    school = st.multiselect("Colegio", 
                        options=schools,
                        placeholder="Todos",
                        )

st.markdown("**Seleccionar Materias**")
col1, col2, col3 = st.columns(3)
with col1:
    basic_courses = st.multiselect("Materias Básicas", 
                        options=courses,
                        placeholder="Todas",
                        )    
    
with col2:
    intermediate_courses = st.multiselect("Materias Intermedias", 
                        options=courses,
                        placeholder="Todas",
                        )

with col3:
    advanced_courses = st.multiselect("Materias Avanzadas", 
                        options=courses,
                        placeholder="Todas",
                        )   

st.write("")

st.markdown("**Seleccionar Horario**")
col1, col2, col3, col4 = st.columns(4)
with col1:
    monday_hours = st.multiselect("Lunes", 
                        options= available_hours,
                        placeholder="Todos"
                        )
with col2:
    tuesday_hours = st.multiselect("Martes", 
                        options=available_hours,
                        placeholder="Todos",
                        )
with col3:
    wednesday_hours = st.multiselect("Miércoles", 
                        options=available_hours,
                        placeholder="Todos",
                        )
with col4:
    thursday_hours = st.multiselect("Jueves", 
                        options=available_hours,
                        placeholder="Todos",
                        )
    
col1, col2, col3 = st.columns(3)
with col1:
    friday_hours = st.multiselect("Viernes", 
                        options=available_hours,
                        placeholder="Todos",
                        )
with col2:
    saturday_hours = st.multiselect("Sábado", 
                        options=available_hours,
                        placeholder="Todos",
                        )
with col3:
    sunday_hours = st.multiselect("Domingo", 
                        options=available_hours,
                        placeholder="Todos",
                        )

    
selected_basic_courses = [course_mapping[c] for c in basic_courses]
selected_intermediate_courses = [course_mapping[c] for c in intermediate_courses]
selected_advanced_courses = [course_mapping[c] for c in advanced_courses]
selected_zones = [zone_mapping[z] for z in zone]

filtered_tutors = [
    tutor for tutor in tutors
    if (
        (len(basic_courses) == 0 or any(c in tutor["elementary"].split(", ") for c in selected_basic_courses))
        and (len(intermediate_courses) == 0 or any(c in tutor["middle"].split(", ") for c in selected_intermediate_courses))
        and (len(advanced_courses) == 0 or any(c in tutor["high"].split(", ") for c in selected_advanced_courses))
        and (len(monday_hours) == 0 or any(p in map_time_to_period(tutor["monday"]) for p in monday_hours))
        and (len(tuesday_hours) == 0 or any(p in map_time_to_period(tutor["tuesday"]) for p in tuesday_hours))
        and (len(wednesday_hours) == 0 or any(p in map_time_to_period(tutor["wednesday"]) for p in wednesday_hours))
        and (len(thursday_hours) == 0 or any(p in map_time_to_period(tutor["thursday"]) for p in thursday_hours))
        and (len(friday_hours) == 0 or any(p in map_time_to_period(tutor["friday"]) for p in friday_hours))
        and (len(saturday_hours) == 0 or any(p in map_time_to_period(tutor["saturday"]) for p in saturday_hours))
        and (len(sunday_hours) == 0 or any(p in map_time_to_period(tutor["sunday"]) for p in sunday_hours))
        and (len(zone) == 0 or any(z in tutor["zone"] for z in selected_zones))
        and (len(school) == 0 or any(s in tutor["school"] for s in schools))
        and (tutor["active"] == "true")
    )
]

st.divider()
if not filtered_tutors:
    st.write("No se encontraron tutores con los filtros seleccionados.")
else:
    for tutor in filtered_tutors:
        open_modal = st.button(tutor["name"], key=tutor["name"])
        modal = Modal(
            "Horario de " + tutor["name"], 
            key="modal"+tutor["name"],
            
            padding=30,   
            max_width=600
        )

        if open_modal:
            modal.open()

        if modal.is_open():
            with modal.container():

                username = fetch_tutor_username(tutor["email"])
                classKind = "presencial" if zone else "virtual"

                container_html = '''
                <div id="my-cal-inline" style= "width: 100%; height: 600px; overflow: auto;"></div>
                '''

                script = '''
                    <script type="text/javascript">
                    (function (C, A, L) {
                        let p = function (a, ar) {
                            a.q.push(ar);
                        };
                        let d = C.document;
                        C.Cal =
                            C.Cal ||
                            function () {
                                let cal = C.Cal;
                                let ar = arguments;
                                if (!cal.loaded) {
                                    cal.ns = {};
                                    cal.q = cal.q || [];
                                    d.head.appendChild(d.createElement("script")).src = A;
                                    cal.loaded = true;
                                }
                                if (ar[0] === L) {
                                    const api = function () {
                                        p(api, arguments);
                                    };
                                    const namespace = ar[1];
                                    api.q = api.q || [];
                                    typeof namespace === "string"
                                        ? (cal.ns[namespace] = api) && p(api, ar)
                                        : p(cal, ar);
                                    return;
                                }
                                p(cal, ar);
                            };
                    })(window, "https://app.cal.com/embed/embed.js", "init");
                    Cal("init", { origin: "https://cal.com" });

                    Cal("inline", {
                        elementOrSelector: "#my-cal-inline",
                        calLink: "userTagName/typeOfClass",
                    });

                    Cal("ui", {
                        styles: { branding: { brandColor: "#000000" } },
                        hideEventTypeDetails: true,
                    });
                    </script>
                '''.replace("userTagName", username).replace("typeOfClass", classKind)

                components.html(container_html + script, height=600)             
