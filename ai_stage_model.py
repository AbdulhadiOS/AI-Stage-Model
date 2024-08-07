#الاستبانة القبلية
import pandas as pd
import numpy as np
import random
from sklearn.cluster import KMeans
from datetime import datetime, timedelta

# Define the list of skills and questions for the post-assessment survey
skills_questions = {
    'AcademicAchievement': 'Rate your Academic Achievement from 1 (Poor) to 5 (Excellent):',
    'ResearchSkills': 'Rate your Research Skills from 1 (Poor) to 5 (Excellent):',
    'ComputerSkills': 'Rate your Computer Skills from 1 (Poor) to 5 (Excellent):',
    'SocialInteractionSkills': 'Rate your Social Interaction Skills from 1 (Poor) to 5 (Excellent):',
    'PresentationSkills': 'Rate your Presentation Skills from 1 (Poor) to 5 (Excellent):',
    'CollaborationTaskCompletion': 'Rate your Collaboration and Task Completion from 1 (Poor) to 5 (Excellent):',
    'LeadershipSkills': 'Rate your Leadership Skills from 1 (Poor) to 5 (Excellent):',
    'TimeManagementSkills': 'Rate your Time Management Skills from 1 (Poor) to 5 (Excellent):',
    'ProblemSolvingSkills': 'Rate your Problem Solving Skills from 1 (Poor) to 5 (Excellent):',
    'CriticalThinkingSkills': 'Rate your Critical Thinking Skills from 1 (Poor) to 5 (Excellent):',
    'WrittenCommunicationSkills': 'Rate your Written Communication Skills from 1 (Poor) to 5 (Excellent):',
    'OrganizationalSkills': 'Rate your Organizational Skills from 1 (Poor) to 5 (Excellent):',
    'DesignThinkingSkills': 'Rate your Design Thinking Skills from 1 (Poor) to 5 (Excellent):',
    'ScientificMethodSkills': 'Rate your Scientific Method Application Skills from 1 (Poor) to 5 (Excellent):',
    'CreativeProblemSolvingSkills': 'Rate your Creative Problem-Solving Skills from 1 (Poor) to 5 (Excellent):'
}

# List of random team names
team_names = [
    'Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet',
    'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango',
    'Uniform', 'Victor', 'Whiskey', 'X-ray', 'Yankee', 'Zulu'
]

# List of random project names
project_names = [
    'Project A', 'Project B', 'Project C', 'Project D', 'Project E'
]

# Generate a random project name and evaluation date
project_name = random.choice(project_names)
evaluation_date = datetime.now().date() - timedelta(days=random.randint(1, 30))

# Collect students' data
num_students = int(input("Enter the number of students: "))
num_teams = int(input("Enter the number of teams: "))

# Ensure there are enough team names for the number of teams
if len(team_names) < num_teams:
    raise ValueError("Not enough team names for the number of teams.")

students_data = []

for i in range(num_students):
    student_id = f"Student_{i+1}"
    student_skills = {'StudentID': student_id}
    for skill in skills_questions.keys():
        # Generate a random rating between 1 and 5
        rating = random.randint(1, 5)
        student_skills[skill] = rating
    students_data.append(student_skills)

# Create a DataFrame from the collected data
students_df = pd.DataFrame(students_data)

# Convert the skills to a numpy array
skills_preferences = students_df[list(skills_questions.keys())].values

# Use KMeans to form balanced teams
kmeans = KMeans(n_clusters=num_teams, random_state=0, n_init=10).fit(skills_preferences)

# Map numerical team labels to random team names
team_labels = kmeans.labels_
team_name_mapping = {i: team_names[i] for i in range(num_teams)}
students_df['Team'] = [team_name_mapping[label] for label in team_labels]

# Ensure balanced teams
def balance_teams(df, num_teams):
    while True:
        team_sizes = df['Team'].value_counts().to_dict()
        min_size = min(team_sizes.values())
        max_size = max(team_sizes.values())

        if max_size - min_size <= 1:
            break

        large_team = max(team_sizes, key=team_sizes.get)
        small_team = min(team_sizes, key=team_sizes.get)

        student_to_move = df[df['Team'] == large_team].sample(1).index[0]
        df.at[student_to_move, 'Team'] = small_team

balance_teams(students_df, num_teams)

# Sort the DataFrame by team for neatness
students_df = students_df.sort_values(by='Team').reset_index(drop=True)

# Save the result to a new CSV file
students_df.to_csv('students_teams.csv', index=False)

print("Students have been successfully assigned to teams!")
print(students_df)

# Generate final report
def generate_report(df, project_name, evaluation_date):
    report = ""
    report += f"Project: {project_name}\n"
    report += f"Evaluation Date: {evaluation_date}\n\n"
    report += "Final Team Assignment Report\n"
    report += "============================\n"
    team_counts = df['Team'].value_counts().sort_index()
    report += "Number of teams: {}\n".format(len(team_counts))
    report += "Teams and their sizes:\n"
    for team, count in team_counts.items():
        report += "- {}: {} members\n".format(team, count)
    report += "\nDetailed Team Members:\n"
    for team in df['Team'].unique():
        report += f"\nTeam {team}:\n"
        team_members = df[df['Team'] == team]
        for _, member in team_members.iterrows():
            report += f"  - {member['StudentID']}\n"
        report += "\nAnalysis:\n"
        report += f"Team: {team}\n"
        report += f"Project: {project_name}\n"
        report += f"Evaluation Date: {evaluation_date}\n"
        for _, member in team_members.iterrows():
            report += f"Member: {member['StudentID']}\n"
            report += "Strengths:\n"
            report += "- Good collaboration between members: Rating 5/5\n"
            report += "- High technical skills: Rating 4/5\n"
            report += "- Effective communication: Rating 4/5\n"
            report += "Weaknesses:\n"
            report += "- Time management: Rating 2/5\n"
            report += "- Planning: Rating 3/5\n"
            report += "Feedback:\n"
            report += "Communication is good among team members.\n"
            report += "Time management needs improvement.\n"
            report += "Planning can be more detailed.\n"
            report += "Recommendations:\n"
            report += "Time Management:\n"
            report += "- Use time management tools like Pomodoro technique.\n"
            report += "- Allocate specific time for each task and adhere to it.\n"
            report += "Planning:\n"
            report += "- Prepare daily and weekly work plans with priority settings.\n"
            report += "- Regularly review the plan to ensure progress.\n"
            report += "\n"
    report += "Summary and General Recommendations:\n"
    report += "Planning:\n"
    report += "- Enhance training on using project planning tools.\n"
    report += "- Prepare clear, detailed plans with clear task distribution.\n"
    report += "Time Management:\n"
    report += "- Train the team on time management techniques like Pomodoro.\n"
    report += "- Organize workshops for effective time management.\n"
    report += "Communication:\n"
    report += "- Enhance use of effective communication platforms.\n"
    report += "- Organize regular meetings to enhance communication and task distribution.\n"
    report += "Collaboration:\n"
    report += "- Encourage teamwork by organizing events and recreational activities.\n"
    report += "- Fairly and equitably distribute tasks among members.\n"
    report += "Practical Recommendations for Improvement:\n"
    report += "- Trainings and Workshops: Organize training workshops to improve planning, time management, and communication skills.\n"
    report += "- Use of Technological Tools: Enhance the use of planning and project management tools.\n"
    report += "- Regular Evaluation Sessions: Organize regular evaluation sessions to review progress and identify areas for improvement.\n"
    return report

# Ask if the user wants to display the final report
display_report = input("Would you like to display the final report? (yes/no): ").strip().lower()
if display_report == 'yes':
    final_report = generate_report(students_df, project_name, evaluation_date)
    print(final_report)

#الاستبانة البعدية
import pandas as pd
import numpy as np
import random
from sklearn.cluster import KMeans
from datetime import datetime, timedelta

# Define the list of skills and questions for the post-assessment survey
skills_questions = {
    'AcademicAchievement': 'Rate your Academic Achievement from 1 (Poor) to 5 (Excellent):',
    'ResearchSkills': 'Rate your Research Skills from 1 (Poor) to 5 (Excellent):',
    'ComputerSkills': 'Rate your Computer Skills from 1 (Poor) to 5 (Excellent):',
    'SocialInteractionSkills': 'Rate your Social Interaction Skills from 1 (Poor) to 5 (Excellent):',
    'PresentationSkills': 'Rate your Presentation Skills from 1 (Poor) to 5 (Excellent):',
    'CollaborationTaskCompletion': 'Rate your Collaboration and Task Completion from 1 (Poor) to 5 (Excellent):',
    'LeadershipSkills': 'Rate your Leadership Skills from 1 (Poor) to 5 (Excellent):',
    'TimeManagementSkills': 'Rate your Time Management Skills from 1 (Poor) to 5 (Excellent):',
    'ProblemSolvingSkills': 'Rate your Problem Solving Skills from 1 (Poor) to 5 (Excellent):',
    'CriticalThinkingSkills': 'Rate your Critical Thinking Skills from 1 (Poor) to 5 (Excellent):',
    'WrittenCommunicationSkills': 'Rate your Written Communication Skills from 1 (Poor) to 5 (Excellent):',
    'OrganizationalSkills': 'Rate your Organizational Skills from 1 (Poor) to 5 (Excellent):',
    'DesignThinkingSkills': 'Rate your Design Thinking Skills from 1 (Poor) to 5 (Excellent):',
    'ScientificMethodSkills': 'Rate your Scientific Method Application Skills from 1 (Poor) to 5 (Excellent):',
    'CreativeProblemSolvingSkills': 'Rate your Creative Problem-Solving Skills from 1 (Poor) to 5 (Excellent):'
}

# List of random team names
team_names = [
    'Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet',
    'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango',
    'Uniform', 'Victor', 'Whiskey', 'X-ray', 'Yankee', 'Zulu'
]

# List of random project names
project_names = [
    'Project A', 'Project B', 'Project C', 'Project D', 'Project E'
]

# Generate a random project name and evaluation date
project_name = random.choice(project_names)
evaluation_date = datetime.now().date() - timedelta(days=random.randint(1, 30))

# Collect students' data
num_students = int(input("Enter the number of students: "))
num_teams = int(input("Enter the number of teams: "))

# Ensure there are enough team names for the number of teams
if len(team_names) < num_teams:
    raise ValueError("Not enough team names for the number of teams.")

students_data = []

for i in range(num_students):
    student_id = f"Student_{i+1}"
    student_skills = {'StudentID': student_id}
    for skill in skills_questions.keys():
        # Generate a random rating between 1 and 5
        rating = random.randint(1, 5)
        student_skills[skill] = rating
    students_data.append(student_skills)

# Create a DataFrame from the collected data
students_df = pd.DataFrame(students_data)

# Convert the skills to a numpy array
skills_preferences = students_df[list(skills_questions.keys())].values

# Use KMeans to form balanced teams
kmeans = KMeans(n_clusters=num_teams, random_state=0, n_init=10).fit(skills_preferences)

# Map numerical team labels to random team names
team_labels = kmeans.labels_
team_name_mapping = {i: team_names[i] for i in range(num_teams)}
students_df['Team'] = [team_name_mapping[label] for label in team_labels]

# Ensure balanced teams
def balance_teams(df, num_teams):
    while True:
        team_sizes = df['Team'].value_counts().to_dict()
        min_size = min(team_sizes.values())
        max_size = max(team_sizes.values())

        if max_size - min_size <= 1:
            break

        large_team = max(team_sizes, key=team_sizes.get)
        small_team = min(team_sizes, key=team_sizes.get)

        student_to_move = df[df['Team'] == large_team].sample(1).index[0]
        df.at[student_to_move, 'Team'] = small_team

balance_teams(students_df, num_teams)

# Sort the DataFrame by team for neatness
students_df = students_df.sort_values(by='Team').reset_index(drop=True)

# Save the result to a new CSV file
students_df.to_csv('students_teams.csv', index=False)

print("Students have been successfully assigned to teams!")
print(students_df)

# Generate final report
def generate_report(df, project_name, evaluation_date):
    report = ""
    report += f"Project: {project_name}\n"
    report += f"Evaluation Date: {evaluation_date}\n\n"
    report += "Final Team Assignment Report\n"
    report += "============================\n"
    team_counts = df['Team'].value_counts().sort_index()
    report += "Number of teams: {}\n".format(len(team_counts))
    report += "Teams and their sizes:\n"
    for team, count in team_counts.items():
        report += "- {}: {} members\n".format(team, count)
    report += "\nDetailed Team Members:\n"
    for team in df['Team'].unique():
        report += f"\nTeam {team}:\n"
        team_members = df[df['Team'] == team]
        for _, member in team_members.iterrows():
            report += f"  - {member['StudentID']}\n"
        report += "\nAnalysis:\n"
        report += f"Team: {team}\n"
        report += f"Project: {project_name}\n"
        report += f"Evaluation Date: {evaluation_date}\n"
        for i, member in enumerate(team_members.iterrows()):
            report += f"Member {i + 1}: {member[1]['StudentID']}\n"
            report += "Strengths:\n"
            report += "- Good collaboration between members: Rating 5/5\n"
            report += "- High technical skills: Rating 4/5\n"
            report += "- Effective communication: Rating 4/5\n"
            report += "Weaknesses:\n"
            report += "- Time management: Rating 2/5\n"
            report += "- Planning: Rating 3/5\n"
            report += "Feedback:\n"
            report += "Communication is good among team members.\n"
            report += "Time management needs improvement.\n"
            report += "Planning can be more detailed.\n"
            report += "Recommendations:\n"
            report += "Time Management:\n"
            report += "- Use time management tools like Pomodoro technique.\n"
            report += "- Allocate specific time for each task and adhere to it.\n"
            report += "Planning:\n"
            report += "- Prepare daily and weekly work plans with priority settings.\n"
            report += "- Regularly review the plan to ensure progress.\n"
            report += "\n"
    report += "Summary and General Recommendations:\n"
    report += "Planning:\n"
    report += "- Enhance training on using project planning tools.\n"
    report += "- Prepare clear, detailed plans with clear task distribution.\n"
    report += "Time Management:\n"
    report += "- Train the team on time management techniques like Pomodoro.\n"
    report += "- Organize workshops for effective time management.\n"
    report += "Communication:\n"
    report += "- Enhance use of effective communication platforms.\n"
    report += "- Organize regular meetings to enhance communication and task distribution.\n"
    report += "Collaboration:\n"
    report += "- Encourage teamwork by organizing events and recreational activities.\n"
    report += "- Fairly and equitably distribute tasks among members.\n"
    report += "Practical Recommendations for Improvement:\n"
    report += "- Trainings and Workshops: Organize training workshops to improve planning, time management, and communication skills.\n"
    report += "- Use of Technological Tools: Enhance the use of planning and project management tools.\n"
    report += "- Regular Evaluation Sessions: Organize regular evaluation sessions to review progress and identify areas for improvement.\n"
    return report

# Ask if the user wants to display the final report
display_report = input("Would you like to display the final report? (yes/no): ").strip().lower()
if display_report == 'yes':
    final_report = generate_report(students_df, project_name, evaluation_date)
    print(final_report)

#استبانة قياس الاثر
import pandas as pd
import numpy as np
import random
from sklearn.cluster import KMeans
from datetime import datetime, timedelta

# Define the list of skills and questions for the post-assessment survey
skills_questions = {
    'AcademicAchievement': 'How would you rate your academic achievement after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'ResearchSkills': 'How would you rate your research skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'ComputerSkills': 'How would you rate your computer skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'SocialInteractionSkills': 'How would you rate your social interaction skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'PresentationSkills': 'How would you rate your presentation skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'CollaborationTaskCompletion': 'How would you rate your collaboration and task completion skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'LeadershipSkills': 'How would you rate your leadership skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'TimeManagementSkills': 'How would you rate your time management skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'ProblemSolvingSkills': 'How would you rate your problem-solving skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'CriticalThinkingSkills': 'How would you rate your critical thinking skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'WrittenCommunicationSkills': 'How would you rate your written communication skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'OrganizationalSkills': 'How would you rate your organizational skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'DesignThinkingSkills': 'How would you rate your design thinking skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'ScientificMethodSkills': 'How would you rate your scientific method application skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?',
    'CreativeProblemSolvingSkills': 'How would you rate your creative problem-solving skills after participating in the work group on a scale of 1 (Poor) to 5 (Excellent)?'
}

# List of random team names
team_names = [
    'Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet',
    'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango',
    'Uniform', 'Victor', 'Whiskey', 'X-ray', 'Yankee', 'Zulu'
]

# List of random project names
project_names = [
    'Project A', 'Project B', 'Project C', 'Project D', 'Project E'
]

# Generate a random project name and evaluation date
project_name = random.choice(project_names)
evaluation_date = datetime.now().date() - timedelta(days=random.randint(1, 30))

# Collect students' data
num_students = int(input("Enter the number of students: "))
num_teams = int(input("Enter the number of teams: "))

# Ensure there are enough team names for the number of teams
if len(team_names) < num_teams:
    raise ValueError("Not enough team names for the number of teams.")

students_data = []

for i in range(num_students):
    student_id = f"Student_{i+1}"
    student_skills = {'StudentID': student_id}
    for skill in skills_questions.keys():
        # Generate a random rating between 1 and 5
        rating = random.randint(1, 5)
        student_skills[skill] = rating
    students_data.append(student_skills)

# Create a DataFrame from the collected data
students_df = pd.DataFrame(students_data)

# Convert the skills to a numpy array
skills_preferences = students_df[list(skills_questions.keys())].values

# Use KMeans to form balanced teams
kmeans = KMeans(n_clusters=num_teams, random_state=0, n_init=10).fit(skills_preferences)

# Map numerical team labels to random team names
team_labels = kmeans.labels_
team_name_mapping = {i: team_names[i] for i in range(num_teams)}
students_df['Team'] = [team_name_mapping[label] for label in team_labels]

# Function to balance teams
def balance_teams(df, num_teams):
    while True:
        team_sizes = df['Team'].value_counts().to_dict()
        min_size = min(team_sizes.values())
        max_size = max(team_sizes.values())

        if max_size - min_size <= 1:
            break

        large_team = max(team_sizes, key=team_sizes.get)
        small_team = min(team_sizes, key=team_sizes.get)

        student_to_move = df[df['Team'] == large_team].sample(1).index[0]
        df.at[student_to_move, 'Team'] = small_team

balance_teams(students_df, num_teams)

# Sort the DataFrame by team for neatness
students_df = students_df.sort_values(by='Team').reset_index(drop=True)

# Save the result to a new CSV file
students_df.to_csv('students_teams.csv', index=False)

print("Students have been successfully assigned to teams!")
print(students_df)

# Generate final report
def generate_report(df, project_name, evaluation_date):
    report = ""
    report += f"Project: {project_name}\n"
    report += f"Evaluation Date: {evaluation_date}\n\n"
    report += "Final Team Assignment Report\n"
    report += "============================\n"
    team_counts = df['Team'].value_counts().sort_index()
    report += "Number of teams: {}\n".format(len(team_counts))
    report += "Teams and their sizes:\n"
    for team, count in team_counts.items():
        report += "- {}: {} members\n".format(team, count)
    report += "\nDetailed Team Members:\n"
    for team in df['Team'].unique():
        report += f"\nTeam {team}:\n"
        team_members = df[df['Team'] == team]
        for _, member in team_members.iterrows():
            report += f"  - {member['StudentID']}\n"
        report += "\nAnalysis:\n"
        report += f"Team: {team}\n"
        report += f"Project: {project_name}\n"
        report += f"Evaluation Date: {evaluation_date}\n"
        for i, member in enumerate(team_members.iterrows()):
            report += f"Member {i + 1}: {member[1]['StudentID']}\n"
            # Generate random strengths and weaknesses
            strengths = random.choices([
                "Good collaboration between members",
                "High technical skills",
                "Effective communication",
                "Quality of work delivered",
                "Commitment to deadlines"
            ], k=3)
            weaknesses = random.choices([
                "Time management",
                "Planning",
                "Communication",
                "Technical skills",
                "Team cooperation"
            ], k=2)
            report += "Strengths:\n"
            for strength in strengths:
                report += f"- {strength}: Rating {random.randint(3, 5)}/5\n"
            report += "Weaknesses:\n"
            for weakness in weaknesses:
                report += f"- {weakness}: Rating {random.randint(1, 3)}/5\n"
            report += "Feedback:\n"
            report += "Communication is good among team members.\n"
            report += "Time management needs improvement.\n"
            report += "Planning can be more detailed.\n"
            report += "Recommendations:\n"
            report += "Time Management:\n"
            report += "- Use time management tools like Pomodoro technique.\n"
            report += "- Allocate specific time for each task and adhere to it.\n"
            report += "Planning:\n"
            report += "- Prepare daily and weekly work plans with priority settings.\n"
            report += "- Regularly review the plan to ensure progress.\n"
            report += "\n"
    report += "Summary and General Recommendations:\n"
    report += "Planning:\n"
    report += "- Enhance training on using project planning tools.\n"
    report += "- Prepare clear, detailed plans with clear task distribution.\n"
    report += "Time Management:\n"
    report += "- Train the team on time management techniques like Pomodoro.\n"
    report += "- Organize workshops for effective time management.\n"
    report += "Communication:\n"
    report += "- Enhance use of effective communication platforms.\n"
    report += "- Organize regular meetings to enhance communication and task distribution.\n"
    report += "Collaboration:\n"
    report += "- Encourage teamwork by organizing events and recreational activities.\n"
    report += "- Fairly and equitably distribute tasks among members.\n"
    report += "Practical Recommendations for Improvement:\n"
    report += "- Trainings and Workshops: Organize training workshops to improve planning, time management, and communication skills.\n"
    report += "- Use of Technological Tools: Enhance the use of planning and project management tools.\n"
    report += "- Regular Evaluation Sessions: Organize regular evaluation sessions to review progress and identify areas for improvement.\n"
    return report

# Ask if the user wants to display the final report
display_report = input("Would you like to display the final report? (yes/no): ").strip().lower()
if display_report == 'yes':
    final_report = generate_report(students_df, project_name, evaluation_date)
    print(final_report)
