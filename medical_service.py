import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='medical_service',
            user='root',
            password=''  # Thay 'your_password' bằng mật khẩu thực tế
        )
        if connection.is_connected():
            print("Connected to the database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

connection = connect_to_database()

if connection is None:
    print("Could not connect to the database.")
else:
    # Thực hiện các thao tác với cơ sở dữ liệu nếu kết nối thành công
    pass


def add_patient(connection):
    cursor = connection.cursor()

    for _ in range(3):  # Thêm 3 bệnh nhân
        full_name = input("Enter patient's full name: ")
        date_of_birth = input("Enter patient's date of birth (YYYY-MM-DD): ")
        gender = input("Enter patient's gender (Male/Female): ")
        address = input("Enter patient's address: ")

        cursor.execute("""
            INSERT INTO patients (full_name, date_of_birth, gender, address)
            VALUES (%s, %s, %s, %s)
        """, (full_name, date_of_birth, gender, address))

    connection.commit()
    print("3 patients have been added.")

def add_doctor(connection):
    cursor = connection.cursor()

    for _ in range(5):  # Thêm 5 bác sĩ
        full_name = input("Enter doctor's full name: ")
        specialization = input("Enter doctor's specialization: ")
        phone_number = input("Enter doctor's phone number: ")
        email = input("Enter doctor's email: ")
        years_of_experience = input("Enter doctor's years of experience: ")

        cursor.execute("""
            INSERT INTO doctors (full_name, specialization, phone_number, email, years_of_experience)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, specialization, phone_number, email, years_of_experience))

    connection.commit()
    print("5 doctors have been added.")

def add_appointments(connection):
    cursor = connection.cursor()

    for patient_id in range(1, 4):  # Thêm 3 cuộc hẹn cho 3 bệnh nhân (patient_id từ 1 đến 3)
        doctor_id = int(input(f"Enter doctor ID for patient {patient_id}: "))
        appointment_date = input("Enter appointment date (YYYY-MM-DD HH:MM:SS): ")
        reason = input("Enter appointment reason: ")

        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, doctor_id, appointment_date, reason))

    connection.commit()
    print("3 appointments have been added.")

def generate_report(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.full_name, p.date_of_birth, p.gender, p.address, d.full_name, a.reason, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)
    
    appointments = cursor.fetchall()

    print("\nAppointment Report:")
    print("No  Patient Name     Birthday  Gender  Address  Doctor Name  Reason   Date")
    print("-" * 80)
    for idx, row in enumerate(appointments, start=1):
        patient_name, dob, gender, address, doctor_name, reason, date = row
        print(f"{idx:2}  {patient_name:<15}  {dob}  {gender:<6}  {address:<10}  {doctor_name:<15}  {reason:<10}  {date}")

from datetime import datetime

def get_appointments_today(connection):
    cursor = connection.cursor()

    # Lấy ngày hiện tại
    today = datetime.today().strftime('%Y-%m-%d')

    cursor.execute("""
        SELECT p.full_name, p.date_of_birth, p.gender, d.full_name, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE DATE(a.appointment_date) = %s
    """, (today,))

    appointments = cursor.fetchall()

    print("\nToday's Appointments:")
    print("No  Patient Name   Birthday  Gender  Doctor Name  Status")
    print("-" * 70)
    for idx, row in enumerate(appointments, start=1):
        patient_name, dob, gender, doctor_name, status = row
        print(f"{idx:2}  {patient_name:<15}  {dob}  {gender:<6}  {doctor_name:<15}  {status}")

def main():
    connection = connect_to_database()
    
    if connection:
        add_patient(connection)
        add_doctor(connection)
        add_appointments(connection)
        generate_report(connection)
        get_appointments_today(connection)
        connection.close()
    else:
        print("Database connection failed.")

if __name__ == "__main__":
    main()
