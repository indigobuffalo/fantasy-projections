1.	Presentation Layer (CLI Interface)
	•	Responsibilities:
	  •	Handle user input (e.g., league and analyst preferences).
	  •	Pass input to the controller and display the processed output.
	•	Components:
	  •	cli.py (or whatever CLI framework you’re using, like argparse or click).
2. Controller Layer
	•	Responsibilities:
	  •	Receive requests from the CLI.
	  •	Interact with the Service Layer to fulfill those requests (e.g., fetching data, performing comparisons).
	  •	Return results to the CLI for display.
	  •	Handle basic input validation before passing requests to services.
	•	Why it’s helpful:
	  •	It centralizes the logic of how the presentation interacts with the business layer.
	  •	Keeps the CLI code cleaner and more focused on user interaction.
	  •	Makes the flow easier to modify in case you need to support multiple interfaces in the future (e.g., a web UI or an API).
	•	Components:
	  •	projection_controller.py: Manages requests related to projections.
	  •	This will invoke services to handle retrieving and comparing projections for the specified analysts and league.
	3.	Service/Business Logic Layer
	•	Responsibilities:
	  •	Perform business logic, such as normalizing and comparing projections.
	  •	Fetch data via the data access layer, but remain agnostic to the data sources.
	•	Components:
	  •	projection_service.py: Handles projection comparisons and normalization.
	  •	league_service.py: Manages which analysts to use per league.
	4.	Data Access Layer
	•	Responsibilities:
	  •	Read from Excel files or other sources and map the data to a consistent format.
	•	Components:
	  •	data_access/excel_reader.py: Extracts data from Excel sheets and ensures consistent data representation.

Example Flow with Controller Layer:

	1.	CLI (Presentation Layer): The user specifies the league and analysts.
	2.	Controller Layer:
	      •	Validates the input and translates it into a request for the Service Layer.
	      •	Calls the appropriate service (e.g., ProjectionController.get_comparisons()).
	3.	Service Layer:
	      •	Retrieves and normalizes the data from the Data Access Layer.
	      •	Compares the projections based on the analysts and league.
	4.	Data Access Layer:
	      •	Reads and maps projections from Excel sheets.
	      •	Returns this data to the service layer for processing.
	5.	Controller Layer: Receives the processed data and passes it back to the CLI.
	6.	CLI: Displays the comparison results to the user.

Benefits of Adding a Controller Layer:

	•	Clearer structure: The CLI doesn’t have to deal with any business logic, and the services don’t handle request orchestration.
	•	Easier testing: The controller layer can be tested in isolation, ensuring that user inputs result in the correct service calls.
	•	Future flexibility: If you later want to add different interfaces (e.g., a web-based UI), the controller layer can remain unchanged, while you just add new “presentation” modules.
