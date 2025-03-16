import pandas as pd

# Load the data
file_path = "admission_data.csv"  # Update this with your actual file path
df = pd.read_csv(file_path)

# Define faculty capacity
faculty_capacity = {'A': 2, 'B': 2, 'C': 2}
faculty_assigned = {'A': [], 'B': [], 'C': []}

# Function to calculate total score based on selection priority
def calculate_total_score(row):
    score = 0
    if row['first selected'] == 'A':
        score += row['score for A'] * 3  # First choice has highest weight
    elif row['first selected'] == 'B':
        score += row['score for B'] * 3
    elif row['first selected'] == 'C':
        score += row['score for C'] * 3

    if row['second selected'] == 'A':
        score += row['score for A'] * 2  # Second choice has medium weight
    elif row['second selected'] == 'B':
        score += row['score for B'] * 2
    elif row['second selected'] == 'C':
        score += row['score for C'] * 2

    if row['third selected'] == 'A':
        score += row['score for A']  # Third choice has lowest weight
    elif row['third selected'] == 'B':
        score += row['score for B']
    elif row['third selected'] == 'C':
        score += row['score for C']

    return score

# Calculate total scores
df['total_score'] = df.apply(calculate_total_score, axis=1)

# Sort applicants by total score in descending order
df_sorted = df.sort_values(by='total_score', ascending=False)

# Assign students to faculties
assignments = []
for _, row in df_sorted.iterrows():
    assigned = None
    for choice in ['first selected', 'second selected', 'third selected']:
        faculty = row[choice]
        if len(faculty_assigned[faculty]) < faculty_capacity[faculty]:  # Check if there is space
            faculty_assigned[faculty].append(row['name'])
            assigned = faculty
            break
    assignments.append(assigned)

# Add assignment results to dataframe
df_sorted['assigned_faculty'] = assignments

# Save the results
output_file = "final_admissions.csv"
df_sorted.to_csv(output_file, index=False)

# Display the assigned applicants
import ace_tools as tools
tools.display_dataframe_to_user(name="Final Admissions", dataframe=df_sorted)
