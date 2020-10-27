## Test Plans (Python)

Description:
This program organizes test plan approvals for multiple levels of management (hierarchy diagram provided in the hierarchy.png file). Different functions such as DFS & BFS are used for the approval process & finding shortest paths. Test plans have different stages, where stages have eligible approvals based on the risk level of the stage:
* Low = The creator can approve. (Don't require approval by manager)
* Moderate = Need to be approved by 1 of the creator's direct managers
* High = Need approval by any 1 of the higher-level managers (direct & indirect managers of the creator's direct managers)

To run program:
Open a terminal inside of the directory where the file is located and enter the command:
##### `py test_plans.py` (may be different terminal command depending on the terminal)

Additional Information:
Example test plan data are initialized in the program. 
The program prints each test plan with the creator, risk level (low, moderate, high), status (complete or incomplete), and the eligible approvers or approver (if stage is completed).
The program also has a function to approve an incomplete stage & checks if the person is a valid approver. This function uses Depth First Search (DFS) to find upper-level managers.
The program also uses Breath First Search (BFS) to find the shortest path of an employee to the CEO.
