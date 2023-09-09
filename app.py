from flask import Flask, render_template, url_for, request, session, redirect, jsonify
import mysql.connector
import plotly.graph_objs as go
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cf896f23169877a843b4e407fb91d9cb' 


def connect_to_database():
    try:
        conn = mysql.connector.connect(user='jimboifyp', password='', host='localhost', port=2020, database='raf')
        print("Connection established successfully")
        return conn
    except mysql.connector.Error as error:
        print("Failed to connect to database: {}".format(error))
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    conn = connect_to_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        print(name)
        print(password)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (name, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['name'] = user['name']
            session['user_id'] = user['user_id']
            role = user['role']
            if role == 'Research Assistant':
                return redirect(url_for('indexRA'))
            elif role == 'Researcher':
                return redirect(url_for('indexR'))
            else:
                return render_template('login.html', error='Invalid role')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    role = request.form['role']
    ic_number = request.form['ic_number']
    gender = request.form['gender']
    education_level = request.form['education_level']
    address = request.form['address']
    contact = request.form['contact']
    
    # Connect to the database
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO users (name, password, email, role, ic_number, gender, education_level, address, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, password, email, role, ic_number, gender, education_level, address, contact)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return "Registration successful"
    else:
        return "Failed to connect to database"
    
    
@app.route('/indexRA')
def indexRA():
    return render_template('indexRA.html')

@app.route('/indexR')
def indexR():
    return render_template('indexR.html')
    
@app.route('/performanceRA')
def performanceRA():
    conn = connect_to_database()
    cursor = conn.cursor()

    user_id = session.get('user_id')

    # Retrieve title_grants for the user_id
    cursor.execute(f"SELECT DISTINCT title_grant FROM save_project")
    title_grants = [row[0] for row in cursor.fetchall()]

    # Retrieve the selected title_grant from the form submission
    title_grant = request.args.get('title_grant')

    query = f"SELECT months, rating, comment FROM performance_table WHERE user_id = '{user_id}' AND project_id IN (SELECT project_id FROM save_project WHERE title_grant = '{title_grant}');"
    cursor.execute(query)
    data = cursor.fetchall()

    # Extract rating and month data from the result
    ratings = [row[1] for row in data]
    months = [row[0] for row in data]
    comments = [row[2] for row in data]

    # Prepare the data in JSON format
    chart_data = {'months': months, 'ratings': ratings}

    query1 = f"SELECT AVG((communication1 + communication2 + communication3) / 3) AS avg_communication, AVG((research_methodology1 + research_methodology2 + research_methodology3) / 3) AS avg_research_methodology, AVG((subject_matter1 + subject_matter2 + subject_matter3) / 3) AS avg_subject_matter, AVG((collaboration1 + collaboration2 + collaboration3) / 3) AS avg_collaboration, AVG((time_management1 + time_management2 + time_management3) / 3) AS avg_time_management FROM skill_radar WHERE user_id = '{user_id}' AND project_id IN (SELECT project_id FROM save_project WHERE title_grant = '{title_grant}');"
    cursor.execute(query1)
    skill_data = cursor.fetchone()

    # Get the project details
    query2 = f"SELECT sp.title_grant, u.name FROM requests AS r JOIN save_project AS sp ON r.project_id = sp.project_id JOIN users AS u ON r.user_id = u.user_id WHERE sp.title_grant = '{title_grant}' AND r.user_id = '{user_id}';"
    cursor.execute(query2)
    project = cursor.fetchone()
    print(project)  # Add this line to check the value of project

    return render_template('performanceRA.html', comments=comments, chart_data=chart_data, skill_data=skill_data, title_grants=title_grants, project=project)

@app.route('/performanceRAReview')
def performanceRAReview():
    conn = connect_to_database()
    cursor = conn.cursor()

    user_id_review = request.args.get('user_id', default=None)
    # Retrieve title_grants for the user_id

    # Retrieve the selected title_grant from the form submission
    title_grant = request.args.get('title_grant')
    query = f"SELECT months, rating, comment FROM performance_table WHERE user_id = '{user_id_review}' AND project_id IN (SELECT project_id FROM save_project WHERE title_grant = '{title_grant}');"
    cursor.execute(query)
    data = cursor.fetchall()

    # Extract rating and month data from the result
    ratings = [row[1] for row in data]
    months = [row[0] for row in data]
    comments = [row[2] for row in data]

    # Prepare the data in JSON format
    chart_data = {'months': months, 'ratings': ratings}

    query1 = f"SELECT AVG((communication1 + communication2 + communication3) / 3) AS avg_communication, AVG((research_methodology1 + research_methodology2 + research_methodology3) / 3) AS avg_research_methodology, AVG((subject_matter1 + subject_matter2 + subject_matter3) / 3) AS avg_subject_matter, AVG((collaboration1 + collaboration2 + collaboration3) / 3) AS avg_collaboration, AVG((time_management1 + time_management2 + time_management3) / 3) AS avg_time_management FROM skill_radar WHERE user_id = '{user_id_review}' AND project_id IN (SELECT project_id FROM save_project WHERE title_grant = '{title_grant}');"
    cursor.execute(query1)
    skill_data = cursor.fetchone()

    # Get the project details
    query2 = f"SELECT sp.title_grant, u.name FROM requests AS r JOIN save_project AS sp ON r.project_id = sp.project_id JOIN users AS u ON r.user_id = u.user_id WHERE sp.title_grant = '{title_grant}' AND r.user_id = '{user_id_review}';"
    cursor.execute(query2)
    project = cursor.fetchone()
    print(project)  # Add this line to check the value of project

    return render_template('performanceRAreview.html', comments=comments, chart_data=chart_data, skill_data=skill_data, title_grants=get_title_grants(), project=project,user_id_review=user_id_review)

@app.route('/profileRA')
def profileRA():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    user_id = session.get('user_id')

    # Retrieve the user's details from the database based on user_id
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Pass the user's details to the template for rendering
    return render_template('profileRA.html', user=user)

@app.route('/profileR')
def profileR():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    user_id = session.get('user_id')

    # Retrieve the user's details from the database based on user_id
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Pass the user's details to the template for rendering
    return render_template('profileR.html', user=user)


@app.route('/projectsR')
def projectsR():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        user_id = session.get('user_id')
        
        # Retrieve projects from the save_project table based on user_id
        select_query = "SELECT project_id, title_grant, research_domain, duration_grant, total_amount, principal_researcher, period_start, period_end, monthly_allowance FROM save_project WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        projects = cursor.fetchall()

        # Close the cursor and database connection
        cursor.close()
        conn.close()

        return render_template('projectsR.html', projects=projects)
    else:
        return "Failed to connect to the database"

# Advertise Research Project route
@app.route('/advertiseR')
def advertise():
    return render_template('advertiseR.html')

@app.route('/save_project', methods=['POST'])
def save_project():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()

        user_id = session.get('user_id')

        title_grant = request.form['title_grant']
        research_domain = request.form['research_domain']
        duration_grant = request.form['duration_grant']
        total_amount = float(request.form['total_amount'])
        principal_researcher = request.form['principal_researcher']
        period_start = datetime.strptime(request.form['period_start'], '%Y-%m-%d').date()
        period_end = datetime.strptime(request.form['period_end'], '%Y-%m-%d').date()
        monthly_allowance = float(request.form['monthly_allowance'])

        # Insert project details into the save_project table
        insert_query = "INSERT INTO save_project (user_id, title_grant, research_domain, duration_grant, total_amount, principal_researcher, period_start, period_end, monthly_allowance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (user_id, title_grant, research_domain, duration_grant, total_amount, principal_researcher, period_start, period_end, monthly_allowance)
        cursor.execute(insert_query, values)

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/projectsR')
    else:
        return "Failed to connect to the database"

@app.route('/projectsRA')
def projects_ra():
    conn = connect_to_database()
    cursor = conn.cursor()
    user_id = session.get('user_id')

    # Retrieve the project details that are available (not associated with any request)
    cursor.execute("""
        SELECT sp.title_grant, sp.research_domain, sp.duration_grant, sp.total_amount, sp.principal_researcher,
        sp.period_start, sp.period_end, sp.monthly_allowance, sp.project_id
        FROM save_project sp
        LEFT OUTER JOIN requests r ON sp.project_id = r.project_id
        WHERE r.project_id IS NULL;

    """)

    projects_available = cursor.fetchall()

    # Retrieve the accepted projects for the logged-in user based on their user_id
    cursor.execute("""
        SELECT ps.*, a.status
        FROM save_project ps
        JOIN requests r ON ps.project_id = r.project_id
        LEFT JOIN approval a ON r.request_id = a.request_id AND a.user_id = %s;

    """, (user_id,))

    your_projects = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('projectsRA.html', projects_available=projects_available, your_projects=your_projects)


@app.route('/request_assistant', methods=['POST'])
def request_assistant():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()

        user_id = session.get('user_id')
        project_id = request.form['project_id']

        # Insert request details into the request table
        insert_query = "INSERT INTO requests (request_id, user_id, project_id) VALUES (NULL, %s, %s)"  # Assuming request_id is auto-incrementing
        values = (user_id, project_id)
        cursor.execute(insert_query, values)

        conn.commit()
        cursor.close()
        conn.close()

        return "Request for an assistant submitted successfully"
    else:
        return "Failed to connect to the database"

@app.route('/approvalRForm', methods=['POST'])
def approval_requests_form():
    if request.method == 'POST':
        # Handle the form submission for accepting or rejecting requests
        request_id = request.form['request_id']
        user_id = request.form['user_id'] 
        action = request.form['action']  # 'accept' or 'reject'

        # Perform the necessary actions based on the request_id and action
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            # Remove the extra closing parenthesis from the SQL query string
            insert_query = "INSERT INTO approval (request_id, status, user_id) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (request_id, action, user_id))

            conn.commit()
            cursor.close()
            conn.close()

        # Redirect to the approval page after processing the request
        return redirect('/approvalR')

@app.route('/approvalR', methods=['GET'])
def approval_requests():
        approval_requests = []

        # Establish a connection to the database
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            # Query the requests and save_project tables to get the necessary data
            cursor.execute("""
                SELECT r.request_id, r.user_id, u.name, sp.title_grant
                FROM requests r
                LEFT JOIN users u ON r.user_id = u.user_id
                LEFT JOIN save_project sp ON r.project_id = sp.project_id
                LEFT JOIN approval a ON r.request_id = a.request_id
                WHERE a.status IS NULL
            """)
            requests = cursor.fetchall()

            user_id_review = None  # Initialize the variable before the loop

            for req in requests:
                request_data = {
                    'request_id': req[0],
                    'user_id_review': req[1],
                    'research_assistant_name': req[2],
                    'title_grant': req[3] if req[3] else 'N/A',
                }
                approval_requests.append(request_data)

                # Update the value of user_id_review if needed
                user_id_review = req[1]

            cursor.close()
            conn.close()

            return render_template('approvalR.html', approval_requests=approval_requests, user_id_review=user_id_review)
        else:
            return "Failed to connect to the database"



@app.route('/ra_evaluateR', methods=['GET', 'POST'])
def ra_evaluateR():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT project_id FROM requests")
        project_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        if request.method == 'POST':
            project_id = request.form['project_id']

            conn = connect_to_database()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM requests WHERE project_id = %s", (project_id,))
                project = cursor.fetchone()
                cursor.close()
                conn.close()

                if project:
                    return render_template('ra_evaluateR.html', project=project, project_ids=project_ids)
                else:
                    return "Invalid project ID"
            else:
                return "Failed to connect to the database"

        return render_template('ra_evaluateR.html', project_ids=project_ids)
    else:
        return "Failed to connect to the database"
    

@app.route('/rating_evaluate', methods=['GET', 'POST'])
def rating_evaluate():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        project_id = request.form.get('project_id')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        date = request.form.get('date')

        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            # Insert rating and comment into the database
            insert_query = "INSERT INTO performance_table (user_id, project_id, rating, comment,months) VALUES (%s, %s, %s, %s,%s)"
            values = (user_id, project_id, rating, comment, date)
            cursor.execute(insert_query, values)

            conn.commit()
            cursor.close()
            conn.close()

            return "Rating and comment submitted successfully"
        else:
            return "Failed to connect to the database"
    else:
        return "Invalid request method"

@app.route('/skill_evaluate', methods=['GET', 'POST'])
def skill_evaluate():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        project_id = request.form.get('project_id')
        communication1 = request.form.get('communication1')
        communication2 = request.form.get('communication2')
        communication3 = request.form.get('communication3')
        research_methodology1 = request.form.get('research_methodology1')
        research_methodology2 = request.form.get('research_methodology2')
        research_methodology3 = request.form.get('research_methodology3')
        subject_matter1 = request.form.get('subject_matter1')
        subject_matter2 = request.form.get('subject_matter2')
        subject_matter3 = request.form.get('subject_matter3')
        collaboration1 = request.form.get('collaboration1')
        collaboration2 = request.form.get('collaboration2')
        collaboration3 = request.form.get('collaboration3')
        time_management1 = request.form.get('time_management1')
        time_management2 = request.form.get('time_management2')
        time_management3 = request.form.get('time_management3')
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            # Insert rating and comment into the database
            insert_query = "INSERT INTO skill_radar (user_id, project_id, communication1, communication2, communication3, research_methodology1, research_methodology2, research_methodology3, subject_matter1, subject_matter2, subject_matter3, collaboration1, collaboration2, collaboration3, time_management1, time_management2, time_management3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (user_id, project_id, communication1, communication2, communication3, research_methodology1, research_methodology2, research_methodology3, subject_matter1, subject_matter2, subject_matter3, collaboration1, collaboration2, collaboration3, time_management1, time_management2, time_management3)
            cursor.execute(insert_query, values)

            conn.commit()
            cursor.close()
            conn.close()

            return "Rating and comment submitted successfully"
        else:
            return "Failed to connect to the database"
    else:
        return "Invalid request method"

@app.route('/commR')
def commR():
    return render_template('commR.html', title_grants=get_title_grants())


def get_title_grants():
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT DISTINCT title_grant FROM save_project;"
    cursor.execute(query)
    title_grants = [row[0] for row in cursor.fetchall()]

    return title_grants

@app.route('/researcher_communication', methods=['GET', 'POST'])
def researcher_communication():
    if request.method == 'POST':
        title_grant = request.form['title_grant']
        selected_title_grant = title_grant

        # Retrieve the project_id based on the selected title grant
        conn = connect_to_database()
        cursor = conn.cursor()

        query = f"SELECT project_id FROM save_project WHERE title_grant = '{title_grant}';"

        cursor.execute(query)
        project_id = cursor.fetchone()

        # Retrieve the user_id based on the project_id from the requests table
        query1 = f"SELECT user_id FROM requests WHERE project_id = '{project_id[0]}';"
        cursor.execute(query1)
        project_request = cursor.fetchone()

        query2 = f"SELECT name,email,contact FROM users WHERE user_id = '{project_request[0]}';"
        cursor.execute(query2)
        assistant_info = cursor.fetchone()

        # Close the database connection after fetching data
        cursor.close()
        conn.close()

        return render_template('commR.html', title_grants=get_title_grants(), assistant_info=assistant_info, selected_title_grant=selected_title_grant)

    return render_template('commR.html', title_grants=get_title_grants())


@app.route('/commRA', methods=['GET', 'POST'])
def communicationRA():
    if request.method == 'POST':
        title_grant = request.form['title_grant']
        # Perform any additional logic or database operations based on the selected title grant
        return render_template('commRA.html', title_grant=title_grant)
    else:
        return render_template('commRA.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)                              