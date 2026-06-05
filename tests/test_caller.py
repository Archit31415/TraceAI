from test_utils import calculate_average_score

def generate_user_report(user_id: int):
    print(f"Fetching data for User {user_id}...")
    
    recent_scores = []
    
    print("Calculating metrics...")
    avg = calculate_average_score(recent_scores)
    
    print(f"Report generated: Average Score = {avg}")

if __name__ == "__main__":
    generate_user_report(1042)