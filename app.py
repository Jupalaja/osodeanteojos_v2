import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

from utils import map_time_to_period
from html_content import container_html, script
from api import fetch_tutors, fetch_tutor_username

from mapping import zone_mapping, course_mapping
from config import zones, schools, courses, available_hours

def main():

    st.title("Oso de anteojos")
    st.text("")
    st.text("")

    st.markdown("**Seleccionar Colegio y Zona**")
    col1, col2 = st.columns(2)
    with col1:
        zone = st.multiselect("Zona",options=zones, placeholder="Todas")  
    with col2:
        school = st.multiselect("Colegio", options=schools, placeholder="Todos")

    st.markdown("**Seleccionar Materias**")
    col1, col2, col3 = st.columns(3)
    with col1:
        basics = st.multiselect("Materias Básicas", options=courses, placeholder="Todas")    
    with col2:
        intemediates = st.multiselect("Materias Intermedias", options=courses, placeholder="Todas")
    with col3:
        advanced = st.multiselect("Materias Avanzadas", options=courses,placeholder="Todas")   

    st.markdown("**Seleccionar Horario**")
    col1, col2, col3 = st.columns(3)
    with col1:
        monday = st.multiselect("Lunes", options=available_hours, placeholder="Todos")
    with col2:
        tuesday = st.multiselect("Martes", options=available_hours, placeholder="Todos")
    with col3:
        wednesday = st.multiselect("Miércoles", options=available_hours, placeholder="Todos")    
        
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        thursday = st.multiselect("Jueves", options=available_hours, placeholder="Todos")
    with col2:
        friday = st.multiselect("Viernes", options=available_hours, placeholder="Todos")
    with col3:
        saturday = st.multiselect("Sábado", options=available_hours, placeholder="Todos")
    with col4:
        sunday = st.multiselect("Domingo", options=available_hours, placeholder="Todos")

        
    selected_basics = [course_mapping[c] for c in basics]
    selected_intemediates = [course_mapping[c] for c in intemediates]
    selected_advanced = [course_mapping[c] for c in advanced]
    selected_zones = [zone_mapping[z] for z in zone]

    tutors = fetch_tutors()

    filtered_tutors = [
        tutor for tutor in tutors
        if (
            (len(basics) == 0 or any(c in tutor["elementary"].split(", ") for c in selected_basics))
            and (len(intemediates) == 0 or any(c in tutor["middle"].split(", ") for c in selected_intemediates))
            and (len(advanced) == 0 or any(c in tutor["high"].split(", ") for c in selected_advanced))
            and (len(monday) == 0 or any(p in map_time_to_period(tutor["monday"]) for p in monday))
            and (len(tuesday) == 0 or any(p in map_time_to_period(tutor["tuesday"]) for p in tuesday))
            and (len(wednesday) == 0 or any(p in map_time_to_period(tutor["wednesday"]) for p in wednesday))
            and (len(thursday) == 0 or any(p in map_time_to_period(tutor["thursday"]) for p in thursday))
            and (len(friday) == 0 or any(p in map_time_to_period(tutor["friday"]) for p in friday))
            and (len(saturday) == 0 or any(p in map_time_to_period(tutor["saturday"]) for p in saturday))
            and (len(sunday) == 0 or any(p in map_time_to_period(tutor["sunday"]) for p in sunday))
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

                    script.replace("userTagName", username).replace("typeOfClass", classKind)
                    components.html(container_html + script, height=600)             

if __name__ == "__main__":
    main()