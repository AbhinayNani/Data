Generating ingredient data:

-Generate a CSV file containing the data for a given list of ingredients.

-main.py

-To run: python main.py output_file “ingredients”

-Eg.: python main.py output.csv "acetonaphthone, butylcyclohexanol, Shea Butter, Cocoa Butter"

-Will generate a CSV file in ‘generated_data’ folder with the name ‘output’.

------------------------------------------------------------------------------------------------------------------
Creating/updating vector database:

-This pipeline works using a vector store stored in the “database” folder. This code helps create that database.

-To update the vector store with new data you need to delete the “database” folder containing the previous data and run this script with the new data stored in a CSV.

-FAISS doesn’t support adding new data to existing vector store so the need to create a new vector store every time.

-create_new_db.py

-To run: python create_new_db.py path/to/dataset.csv

