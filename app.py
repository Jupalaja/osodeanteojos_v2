import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

from utils import map_time_to_period
from api import fetch_tutors, fetch_tutor_username, send_api_key

from mapping import zone_mapping, course_mapping
from config import zones, schools, courses, available_hours

def main():
    def home():
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
                and (len(school) == 0 or any(s in tutor.get("school", "") for s in school))
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

                        script_html = '''
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
                                hideEventTypeDetails: true,
                            });
                            </script>
                        '''.replace("userTagName", username).replace("typeOfClass", classKind)

                        components.html(container_html + script_html, height=600)             

    def apiKey():
        api_key_input = st.text_input("Ingresa una clave API", "")
        submit_button = st.button("Enviar")

        if submit_button:
            if api_key_input:
                response_data = send_api_key(api_key_input)
                if not response_data.get("ok"):
                    st.error(response_data.get("message", "Hubo un error"))
                else:
                    st.success(f"Tutor: {response_data['name']} Agregado")
                    # Show user information as JSON
                    st.json(response_data)
            else:
                st.error("Ingresa una clave API")


    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button('Home'):
            st.session_state['page'] = 'home'

    with col2:
        if st.button('Claves API'):
            st.session_state['page'] = 'apiKey'

    # Initialize session_state
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    # Render the selected page
    if st.session_state['page'] == 'home':
        home()
    elif st.session_state['page'] == 'apiKey':
        apiKey()


if __name__ == "__main__":
    main()