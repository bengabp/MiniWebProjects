import pandas as pd
import random
import faker

# Create a Faker instance for generating random data
fake = faker.Faker()
index = 2
while True:
    # Generate 100 random examples in the specified format
    data = []
    for _ in range(100):
        example = {
            "FirstName": fake.first_name(),
            "Lastname": fake.last_name(),
            "Company_name": fake.company(),
            "Email": fake.email(),
        }
        data.append(example)

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Define the CSV file path where you want to save the DataFrame
    csv_file_path = f"output_data_{index}.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)
    index += 1
    print(f"DataFrame saved to {csv_file_path}")
