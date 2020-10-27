#To run with terminal: enter "py test_plans.py"
#(may be different terminal command depending on the terminal)
from collections import defaultdict
import random

#Seeded organizational hierarchy with 4 levels of management
ceo = 'Zac' # Zac is the CEO (top of hierarchy)
#Employee management: [manager, employee]
employees = [
	['Zac','Xavier'],
	['Zac', 'Yash'],
	['Zac', 'Luke'],
	['Xavier', 'Jackie'],
	['Xavier', 'Katie'],
	['Yash', 'Katie'],
	['Jackie', 'Abby'],
	['Katie', 'Abby'],
	['Katie', 'Bob'],
	['Luke', 'Bob']
]

#turn list into a dictionary
#where key is employee, and value is a list of his/her manager(s)
hierarchy = defaultdict(list)
for parent, child in employees:
	hierarchy[child].append(parent)

#class for Test Plan
class testPlan:
	#initialize properties
	def __init__(self, name):
		self.name = name

	#function to print test plan
	def printPlan(self):
		print(self.name + ":")

#class for Stages of test plans
class Stages:
	#initialize properties
	def __init__(self, name, author, riskLevel, status, approver):
		self.name = name
		self.author = author
		self.riskLevel = riskLevel
		self.status = status
		self.approver = approver

	#function to print stages with details
	def printStage(self):
		#Note: reinitializing list since I didn't want it passed as a property
		#Seeded organizational hierarchy with 4 levels of management
		ceo = 'Zac' # Zac is the CEO (top of hierarchy)
		#Employee management: [manager, employee]
		employees = [
			['Zac','Xavier'],
			['Zac', 'Yash'],
			['Zac', 'Luke'],
			['Xavier', 'Jackie'],
			['Xavier', 'Katie'],
			['Yash', 'Katie'],
			['Jackie', 'Abby'],
			['Katie', 'Abby'],
			['Katie', 'Bob'],
			['Luke', 'Bob']
		]
		#turn list into a dictionary
		#where key is employee, and value is a list of his/her manager(s)
		hierarchy = defaultdict(list)
		for parent, child in employees:
			hierarchy[child].append(parent)

		#Traverse graph using Depth First Search to find upper-level managers
		def dfs(upperLevel, hierarchy, manager):
			#add if indirect manager is not in list
			if manager not in upperLevel:
				upperLevel.append(manager)
				#traverse for more upper-level managers
				for upperManager in hierarchy.get(manager):
					#stop if reach the top of hierarchy
					if (upperManager != ceo):
						dfs(upperLevel, hierarchy, upperManager)

		#get eligible approvers for incomplete stages
		if (self.status == 'incomplete'):
			#if low risk level, author can approve
			if (self.riskLevel == 'low'):
				self.approver = self.author
			#if moderate risk level, direct managers can approve
			elif (self.riskLevel == 'moderate'):
				self.approver = ', '.join(hierarchy.get(self.author))
			#if high risk level, direct managers' direct & indirect managers can approve
			else:
				directManagers = hierarchy.get(self.author)
				upperLevel = []
				#traverse for upper-level managers
				for manager in directManagers:
					#stop search if reaches the top of hierarchy
					if (manager != ceo):
						dfs(upperLevel, hierarchy, manager)
				#add person at top of hierarchy (ceo)
				upperLevel.append(ceo)
				self.approver = ', '.join(upperLevel)

		#print workflow nicely
		print("    " + self.name + ":")
		print("        " + "Created By: " + self.author)
		print("        " + "Risk level: " + self.riskLevel)
		print("        " + "Status: " + self.status)
		#differentiate printing approvers for complete vs incomplete stages
		if (self.status == 'incomplete'):
			print("        " + "Eligible Approvers: " + self.approver)
		else:
			print("        " + "Approver: " + self.approver)

	#Function to approve an incomplete Stage on a Test Plan on behalf of a user.
	def approve(self):
		#convert string to list
		eligibleApprovers = list(self.approver.split(", "))
		#For this assessment, I'm randomly choosing one eligible approver
		potentialApprover = random.choice(eligibleApprovers)
		#validation check: the self.approver list already ensures that
		#the approvers are eligible, therefore just need to check if they
		#are in the list of eligible approvers?
		if potentialApprover in eligibleApprovers:
			self.approver = potentialApprover
		else:
			print(potentialApprover + " is not a valid approver.")
		#save stage's new status
		self.status = 'complete'

#Function to pretty print a Test Plan and its Workflow.
#approvers and eligible approvers are printed with the stage defined in Stages
def printAll(allPlans, plansDict):
	for plan in allPlans:
		plan.printPlan()
		for stage in plansDict.get(plan):
			stage.printStage()
		print()

#Function to find the shortest sequence of managers 
#that connects any given employee to the CEO.
#Traverses graph using Breath First Search method
#References: https://www.geeksforgeeks.org/building-an-undirected-graph-and-finding-shortest-path-using-dictionaries-in-python/
def findCEO(hierarchy, initialEmployee, ceo):
	visited = [] #track visted nodes

	queue = [[initialEmployee]] #for traversing

	#check if employee is already the ceo
	if initialEmployee == ceo:
		print(initialEmployee + " is the CEO")
		return

	#while queue is not empty
	while queue:
		seq = queue.pop(0) #pop from queue (oldest stored element)
		currentEmployee = seq[-1] #gets last visited employee of sequence
		#if the employee has not been visited yet
		if currentEmployee not in visited:
			#get employee's managers
			managers = hierarchy.get(currentEmployee)
			#for every employee in managers list, add to path
			for employee in managers:
				new_seq = list(seq)
				new_seq.append(employee)
				queue.append(new_seq) #add new sequence to queue

				#if ceo is found, print the sequence & end the search
				if employee == ceo:
					niceString = ' --> '.join(new_seq)
					print("Shortest sequence to CEO: " + niceString)
					return

			#add employee to visited so we don't repeat the search
			visited.append(currentEmployee)


allPlans = [] #hold all plans
plansDict = defaultdict(list) #dictionary of plans and stages

#initialize instances with example data.
allPlans.append(testPlan('Flight AB1 Test'))
plansDict[allPlans[0]].append(Stages('Stage 1', 'Abby', 'moderate', 'incomplete', None))
plansDict[allPlans[0]].append(Stages('Stage 2', 'Abby', 'high', 'incomplete', None))
plansDict[allPlans[0]].append(Stages('Stage 3', 'Abby', 'low', 'incomplete', None))
plansDict[allPlans[0]].append(Stages('Stage 4', 'Abby', 'moderate', 'incomplete', None))

allPlans.append(testPlan('Flight AB2 Test'))
plansDict[allPlans[1]].append(Stages('Stage 1', 'Bob', 'low', 'complete', 'Bob'))
plansDict[allPlans[1]].append(Stages('Stage 2', 'Bob', 'moderate', 'incomplete', None))
plansDict[allPlans[1]].append(Stages('Stage 3', 'Bob', 'high', 'incomplete', None))
plansDict[allPlans[1]].append(Stages('Stage 4', 'Bob', 'moderate', 'incomplete', None))

allPlans.append(testPlan('Flight C1 Test'))
plansDict[allPlans[2]].append(Stages('Stage 1', 'Jackie', 'low', 'complete', 'Jackie'))
plansDict[allPlans[2]].append(Stages('Stage 2', 'Jackie', 'high', 'complete', 'Zac'))
plansDict[allPlans[2]].append(Stages('Stage 3', 'Jackie', 'moderate', 'complete', 'Xavier'))

#print
printAll(allPlans, plansDict)

#Have Katie approve Stage 1 of plan Flight AB1 Test
approveStage = plansDict.get(allPlans[0])[0] #grab stage
approveStage.approve() #function defined in Stages class
#Print the updated stage
print("Example: Katie approves Stage 1 of plan Flight AB1 Test")
print("Newly approved stage:")
approveStage.printStage()
print()

#Find shortest sequence from Bob to Zac (CEO)
#Possible paths:
#	Bob --> Katie --> Xavier --> Zac
#	Bob --> Katie --> Yash --> Zac
#	Bob --> Luke --> Zac (shortest path)
print("Shortest path from Bob to Zac (CEO)")
findCEO(hierarchy, 'Bob', ceo)