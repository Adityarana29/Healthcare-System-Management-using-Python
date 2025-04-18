import streamlit as st
import database as db
from patient import Patient
from department import Department
from doctor import Doctor
from prescription import Prescription
from medical_test import Medical_Test
import config
import sqlite3 as sql

# function to verify edit mode password
def verify_edit_mode_password():
    edit_mode_password = st.sidebar.text_input('Enter edit mode password', type = 'password')
    if edit_mode_password == config.edit_mode_password:
        st.sidebar.success('Verified')
        return True
    elif edit_mode_password == '':
        st.empty()
    else:
        st.sidebar.error('Invalid edit mode password')
        return False

# function to verify doctor/medical lab scientist access code
def verify_dr_mls_access_code():
    dr_mls_access_code = st.sidebar.text_input('Enter doctor/medical lab scientist access code', type = 'password')
    if dr_mls_access_code == config.dr_mls_access_code:
        st.sidebar.success('Verified')
        return True
    elif dr_mls_access_code == '':
        st.empty()
    else:
        st.sidebar.error('Invalid access code')
        return False

# function to perform various operations of the patient module (according to user's selection)
def patients():
    st.header('PATIENTS')
    option_list = ['', 'Add patient', 'Update patient', 'Delete patient', 'Show complete patient record', 'Search patient']
    option = st.sidebar.selectbox('Select function', option_list)
    p = Patient()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader('ADD PATIENT')
            p.add_patient()
        elif option == option_list[2]:
            st.subheader('UPDATE PATIENT')
            p.update_patient()
        elif option == option_list[3]:
            st.subheader('DELETE PATIENT')
            try:
                p.delete_patient()
            except sql.IntegrityError:      # handles foreign key constraint failure issue (due to integrity error)
                st.error('This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE PATIENT RECORD')
        p.show_all_patients()
    elif option == option_list[5]:
        st.subheader('SEARCH PATIENT')
        p.search_patient()

# function to perform various operations of the doctor module (according to user's selection)
def doctors():
    st.header('DOCTORS')
    option_list = ['', 'Add doctor', 'Update doctor', 'Delete doctor', 'Show complete doctor record', 'Search doctor']
    option = st.sidebar.selectbox('Select function', option_list)
    dr = Doctor()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader('ADD DOCTOR')
            dr.add_doctor()
        elif option == option_list[2]:
            st.subheader('UPDATE DOCTOR')
            dr.update_doctor()
        elif option == option_list[3]:
            st.subheader('DELETE DOCTOR')
            try:
                dr.delete_doctor()
            except sql.IntegrityError:      # handles foreign key constraint failure issue (due to integrity error)
                st.error('This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE DOCTOR RECORD')
        dr.show_all_doctors()
    elif option == option_list[5]:
        st.subheader('SEARCH DOCTOR')
        dr.search_doctor()

# function to perform various operations of the prescription module (according to user's selection)
def prescriptions():
    st.header('PRESCRIPTIONS')
    option_list = ['', 'Add prescription', 'Update prescription', 'Delete prescription', 'Show prescriptions of a particular patient']
    option = st.sidebar.selectbox('Select function', option_list)
    m = Prescription()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_dr_mls_access_code():
        if option == option_list[1]:
            st.subheader('ADD PRESCRIPTION')
            m.add_prescription()
        elif option == option_list[2]:
            st.subheader('UPDATE PRESCRIPTION')
            m.update_prescription()
        elif option == option_list[3]:
            st.subheader('DELETE PRESCRIPTION')
            m.delete_prescription()
    elif option == option_list[4]:
        st.subheader('PRESCRIPTIONS OF A PARTICULAR PATIENT')
        m.prescriptions_by_patient()

# function to perform various operations of the medical_test module (according to user's selection)
def medical_tests():
    st.header('MEDICAL TESTS')
    option_list = ['', 'Add medical test', 'Update medical test', 'Delete medical test', 'Show medical tests of a particular patient']
    option = st.sidebar.selectbox('Select function', option_list)
    t = Medical_Test()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_dr_mls_access_code():
        if option == option_list[1]:
            st.subheader('ADD MEDICAL TEST')
            t.add_medical_test()
        elif option == option_list[2]:
            st.subheader('UPDATE MEDICAL TEST')
            t.update_medical_test()
        elif option == option_list[3]:
            st.subheader('DELETE MEDICAL TEST')
            t.delete_medical_test()
    elif option == option_list[4]:
        st.subheader('MEDICAL TESTS OF A PARTICULAR PATIENT')
        t.medical_tests_by_patient()

# function to perform various operations of the department module (according to user's selection)
def departments():
    st.header('DEPARTMENTS')
    option_list = ['', 'Add department', 'Update department', 'Delete department', 'Show complete department record', 'Search department', 'Show doctors of a particular department']
    option = st.sidebar.selectbox('Select function', option_list)
    d = Department()
    if (option == option_list[1] or option == option_list[2] or option == option_list[3]) and verify_edit_mode_password():
        if option == option_list[1]:
            st.subheader('ADD DEPARTMENT')
            d.add_department()
        elif option == option_list[2]:
            st.subheader('UPDATE DEPARTMENT')
            d.update_department()
        elif option == option_list[3]:
            st.subheader('DELETE DEPARTMENT')
            try:
                d.delete_department()
            except sql.IntegrityError:      # handles foreign key constraint failure issue (due to integrity error)
                st.error('This entry cannot be deleted as other records are using it.')
    elif option == option_list[4]:
        st.subheader('COMPLETE DEPARTMENT RECORD')
        d.show_all_departments()
    elif option == option_list[5]:
        st.subheader('SEARCH DEPARTMENT')
        d.search_department()
    elif option == option_list[6]:
        st.subheader('DOCTORS OF A PARTICULAR DEPARTMENT')
        d.list_dept_doctors()

# function to implement and initialise home/main menu on successful user authentication
def home():
    db.db_init()        # establishes connection to the database and create tables (if they don't exist yet)
    option = st.sidebar.selectbox('Select module', ['', 'Patients', 'Doctors', 'Prescriptions', 'Medical Tests', 'Departments'])
    if option == 'Patients':
        patients()
    elif option == 'Doctors':
        doctors()
    elif option == 'Prescriptions':
        prescriptions()
    elif option == 'Medical Tests':
        medical_tests()
    elif option == 'Departments':
        departments()

st.set_page_config(page_title="Healthcare Management Dashboard", layout="wide")

# Title
st.title("🏥 Healthcare System Management Dashboard")

# --- Disease and Prevention Section ---
st.header("🦠 Disease Information and Prevention Tips")

diseases = {
    "Diabetes": {
        "description": "A chronic condition affecting the way the body processes blood sugar.",
        "prevention": [
            "Maintain a healthy diet",
            "Exercise regularly",
            "Monitor blood sugar levels",
            "Avoid excessive sugar intake"
        ]
    },
    "Hypertension": {
        "description": "High blood pressure, which increases the risk of heart disease and stroke.",
        "prevention": [
            "Reduce salt intake",
            "Manage stress",
            "Exercise regularly",
            "Avoid smoking and alcohol"
        ]
    },
    "Asthma": {
        "description": "A condition in which your airways narrow and swell, producing extra mucus.",
        "prevention": [
            "Avoid allergens and pollutants",
            "Follow medication plan",
            "Maintain a clean environment",
            "Use air purifiers if needed"
        ]
    },
    "COVID-19": {
        "description": "A viral respiratory illness caused by SARS-CoV-2.",
        "prevention": [
            "Wear masks in crowded places",
            "Wash hands regularly",
            "Maintain social distancing",
            "Get vaccinated and boosted"
        ]
    }
}

# Display disease info
for disease, info in diseases.items():
    with st.expander(f"💊 {disease}"):
        st.markdown(f"**Description:** {info['description']}")
        st.markdown("**Prevention Tips:**")
        for tip in info["prevention"]:
            st.markdown(f"- {tip}")

# --- Infrastructure Section ---
st.header("🏗️ Healthcare Infrastructure")

st.markdown("""
Our hospital is equipped with state-of-the-art facilities to provide world-class medical care:
- 🏥 **500+ Beds** with modern amenities
- 🧪 **Advanced Diagnostic Labs** for accurate testing
- 🚑 **24/7 Emergency Services**
- 🛏️ **ICU & Neonatal Units** with latest monitoring systems
- 💻 **Digital Patient Management System**
- 🌐 **Telemedicine & Remote Consultations**
""")

# --- Medical Team Section ---
st.header("👨‍⚕️ Meet Our Specialized Medical Team")

team = [
    {"name": "Dr. Aisha Mehra", "specialty": "Cardiologist", "experience": "15 years"},
    {"name": "Dr. Rohit Gupta", "specialty": "Endocrinologist (Diabetes)", "experience": "10 years"},
    {"name": "Dr. Anjali Rao", "specialty": "Pulmonologist (Asthma)", "experience": "8 years"},
    {"name": "Dr. Varun Sharma", "specialty": "Emergency Medicine", "experience": "12 years"},
    {"name": "Dr. Neha Patel", "specialty": "Pediatrician", "experience": "9 years"},
]

for doc in team:
    with st.container():
        st.markdown(f"### 👨‍⚕️ {doc['name']}")
        st.markdown(f"**Specialty:** {doc['specialty']}")
        st.markdown(f"**Experience:** {doc['experience']}")

# --- Footer ---
st.markdown("---")
st.markdown("📞 For appointments or queries, contact us at: **+91-123-456-7890** | 📧 **healthcare@hospital.com**")

password = st.sidebar.text_input('Enter password', type = 'password')       # user password authentication
if password == config.password:
    st.sidebar.success('Verified')
    home()
elif password == '':
    st.empty()
else:
    st.sidebar.error('Invalid password')
