from doctest import REPORT_CDIFF
import requests
import ndjson as nd
from datetime import datetime, timedelta
import time
import random
from uuid import uuid4
import csv
import os
from dotenv import load_dotenv

load_dotenv()
TB_TOKEN = os.getenv('TB_TOKEN')
if (TB_TOKEN is None):
    TB_TOKEN = input("No token env var found. Paste your admin token here: ")

costs = {
    'London': {
        'Paris': 30,
        'Chicago': 130,
        'Boston': 90,
        'Seattle': 250
    },
    'Paris': {
        'London': 30,
        'Chicago': 160,
        'Boston': 120,
        'Seattle': 280
    },
    'Chicago': {
        'Paris': 160,
        'London': 130,
        'Boston': 60,
        'Seattle': 150
    },
    'Boston': {
        'Paris': 120,
        'Chicago': 60,
        'London': 90,
        'Seattle': 190
    },
    'Seattle': {
        'Paris': 280,
        'Chicago': 150,
        'Boston': 190,
        'London': 250
    }
}


def chance(probability):
    return random.random() < probability


def load_repeat_customers():
    with open('fake_names.csv') as csvfile:
        return list(csv.reader(csvfile))


repeat_customers = load_repeat_customers()

first_names = ["Noah", "Robert", "Jeanette", "Megan", "James", "Henry", "Jessica", "Rebecca", "Gregory", "Jeremy", "Joseph", "Lawrence", "Angela", "Melinda", "William", "Jennifer", "Ricky", "Austin", "Cynthia", "Joel", "Thomas", "Ruth", "Kenneth", "Krista", "Jerry", "Courtney", "Todd", "Rebecca", "Kathleen", "Heather", "Haley", "Tracy", "Adrienne", "Suzanne", "Katherine", "John", "Craig", "Julie", "Jennifer", "Lisa", "Bryan", "David", "Kimberly", "Brandi", "Stephanie", "Judith", "Alicia", "Eric", "Leah", "Kelly", "Matthew", "Nicole", "Virginia", "Brianna", "Kimberly", "Travis", "David", "Sarah", "Krista", "Anthony", "Brian", "William", "Shawn", "Adam", "Lisa", "Lauren", "Ronnie", "David", "Kari", "Elizabeth", "Maria", "Charles", "Collin", "Victoria", "Chase", "Shannon", "Matthew", "Patricia", "Joshua", "Linda", "Daniel", "Sarah", "Kristine", "Todd", "Heidi", "Christina", "Joshua", "Jennifer", "Eric", "Stacey", "Michael", "Breanna", "Keith", "Kristina", "Daniel", "Cassandra", "Lucas", "Michael", "Jennifer", "Michael", "Megan", "Thomas", "Greg", "Stephen", "Angela", "Janet", "Christine", "Andrea", "Tracey", "Amy", "Tamara", "Denise", "Yvette", "Jasmine", "Jessica", "Jason", "Veronica", "Stephanie", "Joanne", "Jonathon", "Michael", "Michael", "Alicia", "Cameron", "Billy", "Michele", "Karen", "Suzanne", "Deborah", "Jason", "Lauren", "Matthew", "Adam", "Louis", "Jason", "Shaun", "Timothy", "Casey", "Jamie", "Megan", "Anthony", "Stephen", "Jennifer", "Timothy", "Zachary", "Robert", "Tony", "Karen", "Jason", "Steven", "Jason", "Jeremy", "Joan", "Brett", "Sarah", "Matthew", "Deborah", "Albert", "Justin", "Frances", "Mary", "William", "Kevin", "Courtney", "Melissa", "David", "Deborah", "Sherry", "Maria", "Kyle", "Miss", "Monique", "Joanna", "Sergio", "Alexander", "Bradley", "Brenda", "Peter", "Paul", "Carlos", "Michele", "Alexandria", "Colleen", "Timothy", "Brianna", "Nicole", "Gloria", "Michael", "Charles", "Jackson", "Christopher", "Deborah", "Tonya", "Joseph", "Tasha", "Donald", "Renee", "Christine", "Matthew", "Laura", "Sean", "Shane", "April", "Jennifer", "Jason", "Erin", "Miss", "Robert", "Derrick", "Timothy", "Joseph", "Tracy", "Amy", "Paul", "Anthony", "Matthew", "Elizabeth", "Amanda", "Angela", "Jesus", "Haley", "Adrian", "Charlene", "William", "Richard", "Tara", "David", "Robert", "Michael", "Brett", "Tanner", "Jessica", "Patricia", "Shaun", "Bradley", "Jason", "Dylan", "Courtney", "Michael", "Theresa", "Hannah", "Matthew", "Elizabeth", "Allison", "April", "John", "Stephanie", "Keith", "Rebecca", "Eric", "Justin", "Kathryn", "Jessica", "John", "Ryan", "Kendra", "Cassandra", "John", "Corey", "Edward", "Hailey", "John", "Wendy", "Renee", "Erin", "Sarah", "Joan", "Jamie", "Maria", "Thomas", "Tiffany", "Kyle", "Matthew", "Raymond", "Mark", "Marissa", "Heather", "Kevin", "Eric", "Daniel", "Rachel", "Alexis", "Jeffrey", "Shane", "Nicole", "Shannon", "Jose", "Caitlin", "Patrick", "Steven", "Michelle", "Ryan", "Nicholas", "Ann", "Karen", "Diane", "Richard", "Kaitlyn", "Stephanie", "Nancy", "Daniel", "Bianca", "Mary", "Leah", "Zachary", "Heidi", "Mitchell", "Vanessa", "Richard", "Amanda", "Jason", "Abigail", "Sandra", "Donna", "Jill", "Holly", "Hannah", "Marissa", "Jennifer", "Jeffrey", "Lauren", "Gail", "David", "Jackson", "Allison", "Karen", "Mariah", "Barbara", "Pamela", "John", "Sydney", "Patrick", "Vanessa", "Danny", "Victor", "Louis", "Christine", "Erika", "Vanessa", "Jonathan", "Sarah", "Leah", "Charles", "Charles", "Daniel", "Bryce", "Stephen", "Lori", "Stephanie", "Courtney", "Ashley", "Sandra", "Amber", "Tamara", "Ashley", "Lauren", "Sara", "Jamie", "Jason", "Carolyn", "Julie", "Randy", "Danielle", "Courtney", "Megan", "David", "William", "Matthew", "Steven", "Matthew", "Joshua", "Robert", "Brenda", "Jessica", "Kristy", "Blake", "Glen", "Scott", "Diane", "Jaime", "Kyle", "Dana", "David", "Diana", "Joseph", "Rodney", "Kenneth", "Virginia", "Gregory", "Michelle", "Terri", "Donna", "Anna", "Blake", "Diane", "Elizabeth", "Donald", "Emily", "Jacob", "Matthew", "Christopher", "Tammy", "Tara", "Mark", "Jonathan", "Amanda", "Linda", "Amy", "Kathleen", "John", "Dennis", "Suzanne", "Mark", "William", "Ashley", "Marcus", "Katherine", "Rebecca", "Shannon", "Anna", "Cathy", "Thomas", "Natasha", "Amanda", "Charlene", "Cody", "Walter", "Diamond", "Benjamin", "Kelsey", "Dana", "Jodi", "Angela", "William", "Kenneth", "Julie", "Stacey", "Gary", "Vicki", "Melissa", "Shannon", "Mike", "Jacob", "Jasmine", "Douglas", "Dakota", "Victoria", "Ethan", "Scott", "Diane", "Kendra", "Jonathan", "Matthew", "Kristine", "Theresa", "Vanessa", "Thomas", "Jessica", "Jesse", "Robert", "Jason", "Julie", "Claudia", "Jason", "Timothy", "Jessica", "Daniel", "Debra", "Daniel", "Ashley", "Krista", "Juan", "Rachael", "Rebecca", "Amanda", "Alexandria", "Amy", "Laura", "Elizabeth", "Chelsey", "Allen", "Melissa", "Nancy", "Wendy", "Danielle", "Robin", "Kevin", "Timothy", "Stephanie", "Emily", "Devin", "Daniel", "Kristopher", "Kimberly", "Zoe", "Kristina", "Carla", "Sean",
               "Stacey", "Stephanie", "Nicole", "April", "Nicole", "Pamela", "Casey", "Jeremiah", "Jose", "Robin", "Claudia", "John", "Brandon", "Courtney", "Michelle", "Benjamin", "Kenneth", "Cynthia", "Megan", "Jill", "Taylor", "Richard", "Jackie", "Darren", "Kristina", "Lori", "Darrell", "Kathleen", "Elizabeth", "Joshua", "Sonya", "Jonathan", "Tara", "Laura", "Sarah", "Daniel", "Daniel", "Scott", "Kayla", "Keith", "William", "Lori", "Jason", "Thomas", "Jody", "Oscar", "Jason", "Rick", "Samuel", "Pamela", "Kathryn", "Brian", "Laura", "Sheila", "Steven", "Jennifer", "Teresa", "Samantha", "Kelly", "Dorothy", "Richard", "Roger", "David", "Shannon", "Dominique", "Andrew", "Jennifer", "Brian", "William", "Vincent", "Craig", "Kimberly", "Phillip", "Benjamin", "William", "Kevin", "Laura", "Thomas", "Sara", "Michael", "Brandon", "Stephen", "Derek", "Stacie", "James", "Leonard", "Robert", "Kevin", "Kathy", "Johnny", "Manuel", "Maria", "Erica", "Tammy", "Jonathan", "Michael", "Rhonda", "David", "Whitney", "Robert", "Shannon", "Chad", "Paul", "Jamie", "Linda", "Mark", "Ryan", "Jacqueline", "Jonathan", "Brenda", "Jason", "Candace", "Juan", "Alexandra", "Thomas", "Stephanie", "Keith", "Shawn", "Jonathan", "Emily", "Zachary", "Brandi", "Mary", "Ashley", "Briana", "Robin", "Laurie", "Tracy", "Michael", "Steve", "Peter", "Joshua", "Bobby", "Angela", "Roy", "Adam", "Kristine", "Jennifer", "Raymond", "Alan", "Mario", "Jason", "Benjamin", "Joseph", "Edward", "Jennifer", "Jesse", "Thomas", "Gerald", "Scott", "Rachael", "Valerie", "Shannon", "Christopher", "Fernando", "Kathryn", "Jennifer", "Aaron", "Chelsea", "Angela", "Rhonda", "Beth", "Edward", "Sherri", "Zoe", "Victoria", "Johnny", "Dorothy", "Olivia", "Daniel", "Patrick", "Debra", "Jessica", "Brianna", "Mario", "Donna", "Amber", "Sean", "Ashley", "Chad", "Clifford", "Billy", "Michael", "Lisa", "Joann", "Jesse", "Alan", "Peter", "Seth", "Andrew", "Lisa", "Amber", "Jacob", "Angela", "James", "Michele", "Miranda", "Randy", "Jennifer", "Candice", "Courtney", "Elizabeth", "Christopher", "Jacqueline", "Donald", "Joseph", "Lauren", "Deanna", "Garrett", "Ana", "Tiffany", "Michael", "Leslie", "Emily", "Rebecca", "Leslie", "Crystal", "Jonathan", "Molly", "Nancy", "Laura", "Joseph", "Erika", "Sarah", "Bryan", "Noah", "Joseph", "Ashley", "Amy", "Amy", "Bradley", "Rebecca", "Tyler", "Chad", "Tyler", "Briana", "Keith", "Lisa", "Sharon", "Maureen", "Cynthia", "Amanda", "Michael", "James", "Lisa", "Alan", "James", "Dana", "Jill", "Cynthia", "Elizabeth", "Justin", "Martin", "Peggy", "James", "Karen", "Brandon", "James", "Jamie", "Theresa", "Tony", "Carlos", "Melissa", "Ryan", "James", "Erica", "Amber", "Carly", "Erika", "Taylor", "Shane", "James", "Heather", "John", "Ann", "Ashley", "Tyler", "Lindsey", "Christopher", "Tracy", "Christine", "Christopher", "Amanda", "Marc", "Sandra", "Tara", "Troy", "Brianna", "Jacob", "Teresa", "Kimberly", "Juan", "Lori", "Mary", "Lori", "Becky", "Shirley", "Elizabeth", "Adam", "Rachel", "Jennifer", "Gina", "Colin", "Michael", "Nicholas", "Erika", "Wayne", "Colleen", "Philip", "Lisa", "Patrick", "Rebecca", "Jennifer", "Kathleen", "John", "Nicole", "Cynthia", "Elizabeth", "Erin", "Lauren", "Faith", "Danielle", "Amy", "Scott", "Christopher", "Autumn", "Glenda", "Brian", "Matthew", "Laura", "Darren", "Patricia", "Anthony", "Sharon", "Michael", "Miranda", "Amanda", "Mark", "Dana", "Stanley", "Tiffany", "Shannon", "Ashley", "Beth", "Robert", "Michael", "Nicole", "Miss", "Benjamin", "Nathan", "Joseph", "Leslie", "Hannah", "Michael", "Aaron", "Angela", "Stacy", "Melissa", "Timothy", "Laurie", "Nicholas", "Sarah", "Shelia", "Debbie", "Thomas", "Laura", "Charles", "Hannah", "Donna", "Joseph", "Kyle", "Lance", "Brendan", "Cole", "Marie", "Gregory", "Amber", "Jeffrey", "Gabriel", "Ronnie", "Laurie", "Zoe", "Kendra", "Jason", "Jennifer", "Anthony", "Matthew", "Ronald", "Willie", "Susan", "Billy", "Valerie", "Derrick", "Jeremy", "Sandra", "Katherine", "Megan", "Michael", "Denise", "Samantha", "Daniel", "Terry", "Juan", "Andrew", "Amanda", "Michael", "Peter", "Ashley", "Jason", "Scott", "William", "Jennifer", "Nicole", "Kathryn", "Martin", "Susan", "Virginia", "Alejandro", "Stephanie", "David", "William", "Sarah", "April", "Christina", "Calvin", "Brittany", "Scott", "Sonia", "Chad", "Christopher", "Susan", "Jennifer", "Michael", "Stephen", "Christina", "Jon", "Gary", "Amanda", "Michael", "Bryan", "Jill", "Gregory", "Jon", "William", "Jonathan", "Malik", "Diane", "Jennifer", "Rita", "Aaron", "Tyler", "Amy", "Christopher", "Sandy", "Kimberly", "Thomas", "Dylan", "James", "Mary", "Christopher", "Frederick", "Travis", "Robert", "Lisa", "Brenda", "Cody", "April", "Cynthia", "Kelly", "Carolyn", "Adam", "Jenna", "Kendra", "Valerie", "Jessica", "Miguel", "Angela", "Daryl", "Dana", "James", "Brian", "Chelsea", "Chad", "Elizabeth", "Amy", "Katherine", "Deborah", "Bonnie", "April", "Lisa", "Michael", "John", "Jessica", "Jack", "Walter", "Matthew", "Dennis", "Jordan", "Randy", "Carrie", "Donna", "Jessica", ]
last_names = ["Tucker", "Ford", "Hawkins", "Drake", "Costa", "Mason", "Martinez", "Golden", "Campbell", "Mendoza", "Holloway", "Roberson", "Smith", "Rollins", "Hunt", "Johnson", "Gonzales", "Brady", "Franklin", "Kim", "Sanford", "Reed", "Benson", "Patterson", "Bishop", "Davidson", "Price", "Richardson", "Wright", "Taylor", "Robles", "Archer", "Lloyd", "Scott", "Miller", "Jordan", "Dickerson", "Garcia", "Walls", "Kennedy", "Watkins", "Norman", "Durham", "Gonzales", "Rivas", "Nelson", "Sanders", "Olson", "Bush", "Leonard", "Woods", "Dean", "Fritz", "Cox", "Kelly", "Adams", "Rivera", "Jacobs", "Owens", "Hawkins", "Winters", "Lewis", "Brown", "Douglas", "Taylor", "Miller", "Bailey", "Bennett", "Khan", "Russell", "Alexander", "Day", "Mullins", "Baker", "Marks", "Camacho", "Pruitt", "Marsh", "Hebert", "Forbes", "Henry", "Hurley", "Marshall", "Price", "Rogers", "Henson", "Williams", "Brown", "Carr", "Bond", "Mullen", "Henry", "Bush", "Johnson", "Mccann", "Morris", "Glover", "Patrick", "Johnson", "Sparks", "King", "Ruiz", "Ibarra", "Parks", "Jimenez", "Smith", "Robinson", "Wise", "Castro", "Hansen", "Smith", "Chavez", "Brown", "Ellis", "Williams", "Cortez", "Anderson", "Murray", "Hoffman", "Williams", "Hughes", "Williams", "Rodriguez", "Howard", "Graves", "Murphy", "Allen", "Jimenez", "Lane", "Padilla", "Hernandez", "Holland", "Morales", "Berry", "Sharp", "Foster", "Patel", "Glass", "Jones", "Perez", "Mcgee", "Alvarez", "Charles", "Campos", "Prince", "Black", "Kirby", "Morales", "Molina", "Patel", "Cortez", "Baldwin", "Blackwell", "Brock", "Reed", "Nelson", "Bright", "Long", "Hancock", "Harris", "Perry", "Bass", "Meyer", "Page", "Lloyd", "Adams", "Knox", "Wilson", "Johnson", "Rodgers", "Emily", "Robertson", "Howard", "Wood", "Howard", "David", "Ross", "Strong", "Wade", "Coleman", "Sullivan", "Roberts", "Le", "Brooks", "Faulkner", "White", "Morris", "Walter", "Maxwell", "George", "White", "Thomas", "Clark", "Jensen", "Mills", "Russo", "Jimenez", "Wright", "Barber", "Ball", "Hawkins", "Wong", "Chavez", "Hayden", "May", "Sandoval", "Erika", "Smith", "Miller", "Franklin", "Johnson", "Bush", "Summers", "Shields", "Cooper", "Stevens", "Lee", "Hudson", "Lewis", "Cooper", "Collins", "Meyer", "Fleming", "Maynard", "Murphy", "Simpson", "Bryant", "King", "Soto", "Lewis", "Park", "Harrell", "Williams", "Stokes", "Mitchell", "Whitaker", "Porter", "Oliver", "Koch", "Hunt", "Mccarthy", "Mcdaniel", "Gomez", "Perez", "Johnson", "Johnson", "Smith", "Thornton", "Hull", "Mccormick", "Oconnor", "Owen", "Macias", "Lee", "Lucas", "Holmes", "Sanchez", "Shaw", "Phillips", "Ramirez", "Benjamin", "Ortiz", "Banks", "Anderson", "Oneill", "Cochran", "Bryan", "Meadows", "Ortiz", "Sanchez", "Gregory", "Mitchell", "Myers", "Smith", "Arnold", "Warren", "Cooper", "Braun", "Matthews", "Gallegos", "Campbell", "Davis", "Pineda", "Mitchell", "Blackwell", "Gutierrez", "Alexander", "Hansen", "Roth", "Herring", "Thomas", "Page", "Smith", "Gonzalez", "Nelson", "Collins", "Beck", "Campbell", "Henry", "Smith", "Mosley", "Flores", "Cochran", "Johnson", "Barnes", "Tyler", "Gutierrez", "Kirk", "Small", "Fuller", "Ford", "Avery", "Powers", "Knight", "Raymond", "Chavez", "White", "Gomez", "Hall", "Wells", "Mcfarland", "Mcguire", "Mills", "Gill", "Warren", "Washington", "Adams", "Sullivan", "Cortez", "Butler", "Pena", "Oliver", "Perkins", "Miller", "Evans", "Anderson", "Lane", "Thompson", "Hurst", "Barber", "Evans", "Boone", "Warren", "Brown", "Miller", "Green", "Collins", "Simon", "Morrow", "Young", "Maldonado", "Carroll", "Garcia", "Johnson", "Williams", "Clark", "Schneider", "Daniels", "Small", "Rios", "Browning", "Garcia", "Vazquez", "Hughes", "Chase", "Rojas", "Garcia", "Callahan", "Collins", "Gibson", "Sawyer", "Turner", "Singh", "Freeman", "Schmidt", "Hays", "Harper", "Black", "Moreno", "Miller", "Mathews", "Thompson", "Lopez", "Bartlett", "Rangel", "Chambers", "Dunn", "Schmidt", "Acevedo", "Smith", "Taylor", "Levine", "Reeves", "Navarro", "Mitchell", "Jones", "Evans", "Davis", "Gonzales", "Burke", "Murphy", "Patterson", "Morris", "Hartman", "Hughes", "Becker", "Cortez", "Baker", "Ferrell", "Chang", "Stein", "Williams", "Hansen", "Stevens", "Ward", "Green", "Booker", "Pope", "Erickson", "Green", "Myers", "Calderon", "Walsh", "Henderson", "Morales", "Romero", "Alvarez", "Foster", "Medina", "Bauer", "Price", "Burke", "Harris", "Evans", "Johnson", "Evans", "Farley", "Coleman", "Robertson", "Roberts", "Johnson", "Best", "White", "Morris", "Thomas", "Walker", "Baker", "Maldonado", "Whitney", "Estrada", "Jenkins", "Gilbert", "Ray", "Hardy", "Hardin", "Welch", "Jones", "Phillips", "Carter", "Adams", "Joseph", "Gardner", "Thompson", "Yang", "Holt", "Leonard", "Watkins", "Velasquez", "Holt", "Rivera", "Parsons", "James", "Ramos", "James", "Roberts", "Parks", "Wilkerson", "Butler", "Brooks", "Sutton", "Wright", "Peterson", "Rodriguez", "Harris", "Page", "Martinez", "Knight", "Mccoy", "Jackson", "Mann", "Davis", "Ramirez", "Williams", "Sanchez", "Mcdonald", "Shaw", "Jennings", "Davis", "Burns", "Maynard", "English", "Stewart",
              "Tucker", "Frye", "Macdonald", "Franklin", "Sherman", "Perkins", "Gomez", "Miller", "Hale", "Jones", "Boyd", "Ramirez", "Rodriguez", "Cannon", "Moore", "Lewis", "Johnson", "Yates", "Vincent", "Johnson", "Callahan", "Alvarado", "Goodman", "Adams", "Jackson", "Miller", "Castillo", "Hodge", "Bailey", "Johnson", "Gray", "Howard", "Castillo", "Adams", "Medina", "Baker", "Graves", "Thompson", "Davis", "Green", "Cook", "Garcia", "Ross", "Mcdonald", "Marshall", "Murray", "Wagner", "Mcgee", "Adams", "Cantrell", "Jones", "Thomas", "Perez", "Smith", "Sellers", "Hoover", "Cook", "Chan", "Mendoza", "Martin", "Bennett", "Reeves", "Cobb", "Johnson", "Smith", "Valencia", "Johnson", "White", "Wyatt", "Campbell", "Hernandez", "Suarez", "Berry", "Mcbride", "Duke", "Fox", "Morris", "Johnson", "Hamilton", "Austin", "Taylor", "Hampton", "Love", "Smith", "Wiggins", "Vaughn", "Blair", "Davenport", "Walker", "Vargas", "Rodriguez", "Butler", "Chandler", "Oneal", "Harris", "Walker", "Osborn", "Williams", "Lewis", "Dennis", "Reyes", "Patton", "Murphy", "Carter", "Robertson", "Rios", "Miller", "Patterson", "Sims", "Jackson", "Black", "Combs", "Russell", "Johnson", "Griffin", "Esparza", "Thompson", "Hall", "Rich", "Williams", "Giles", "Bates", "Brown", "Rivera", "Carter", "Williams", "Mitchell", "Adams", "Walker", "Arias", "Jones", "Wilcox", "Smith", "Hunter", "Bailey", "Campbell", "Clarke", "West", "Brown", "Roth", "Chen", "Sullivan", "Cisneros", "Miles", "Vazquez", "Fischer", "Bryant", "Rowe", "Williams", "Jackson", "Thomas", "Gonzalez", "Li", "Murphy", "Lambert", "Stewart", "Walton", "Drake", "Mckinney", "Goodman", "Henderson", "Le", "Beck", "Johnson", "Marshall", "Nelson", "Love", "Gallagher", "Wright", "Meza", "Williams", "Snyder", "Santiago", "Martinez", "Preston", "Cobb", "Smith", "Morgan", "Phillips", "Walsh", "Church", "Massey", "Vazquez", "Page", "Mccormick", "Hughes", "Obrien", "Marquez", "Willis", "Dickerson", "Barrett", "Garcia", "Williams", "Sanchez", "Berry", "Nunez", "Johnson", "Baldwin", "Booker", "Gallegos", "Hopkins", "Sheppard", "Campos", "Walker", "Williams", "Lowe", "Archer", "Young", "Buck", "Gates", "Long", "Stephens", "Russell", "Rodriguez", "Harris", "Lindsey", "Johnson", "Romero", "Vaughn", "Cooper", "Blankenship", "Jones", "White", "Williams", "Stark", "Green", "Gutierrez", "Vega", "Bennett", "Nguyen", "Perez", "Holder", "Maldonado", "Gilbert", "Carter", "Jackson", "Molina", "Harmon", "Potter", "Greer", "Ballard", "Gutierrez", "White", "Sanchez", "Harris", "Barnett", "Ballard", "Peck", "Ramirez", "Reynolds", "Lee", "Lawson", "Ayala", "Cochran", "Reese", "Brooks", "Spencer", "Norris", "Thomas", "Crawford", "Kidd", "Sanchez", "Pham", "Meyer", "Chavez", "Day", "Cunningham", "Pollard", "Kelly", "Campbell", "Hall", "White", "Larsen", "Mclaughlin", "Martinez", "Browning", "Tucker", "Perry", "Smith", "Nelson", "Goodman", "Mcbride", "Jones", "York", "Mckinney", "White", "Marshall", "Moore", "Anderson", "Kennedy", "Lee", "Montes", "Juarez", "Smith", "Henson", "Campbell", "Morales", "Singleton", "Bowers", "Evans", "Brown", "Obrien", "James", "Rodriguez", "Martinez", "Anderson", "Walsh", "Guerra", "Velasquez", "Macdonald", "Clark", "Hatfield", "Wright", "Montoya", "Larson", "Vaughn", "Shelton", "Johnson", "Thompson", "Barnett", "Hull", "Schroeder", "Smith", "Armstrong", "Gibson", "Alexander", "Summers", "Chavez", "Allison", "Lee", "Wilson", "White", "Costa", "Johnson", "Carroll", "Hardy", "James", "Fisher", "Moore", "Torres", "Sullivan", "Riley", "Martin", "Gabrielle", "Mcknight", "Watts", "Reyes", "Lopez", "Calderon", "Roberson", "Cooper", "Ellis", "Love", "Diaz", "Heath", "Lowery", "Joseph", "Manning", "Ferguson", "Jones", "Hendrix", "White", "Gomez", "Farmer", "Williams", "Stein", "Jones", "Newton", "Weber", "Rogers", "Shannon", "Thompson", "Robertson", "Flynn", "Mckinney", "Ramirez", "Ramirez", "Adams", "Caldwell", "Davis", "James", "Drake", "Mueller", "Moreno", "Harding", "Smith", "Lara", "Collins", "Hernandez", "Villarreal", "Dunn", "Lane", "Kim", "Bowman", "Aguilar", "Allen", "Castaneda", "Gray", "Juarez", "Baker", "Gentry", "Smith", "Klein", "Davis", "Reynolds", "Williams", "Murphy", "Harper", "Bailey", "Cochran", "Ortiz", "Thompson", "King", "Davis", "Harper", "Hale", "Williams", "Adams", "Parker", "Hudson", "Mcmillan", "Hardy", "Douglas", "Rodriguez", "Turner", "Parker", "Salazar", "Brown", "Vasquez", "Allison", "Perez", "Patel", "Stark", "Hall", "Cannon", "Munoz", "Wang", "Schwartz", "Kramer", "Fritz", "Mora", "Bailey", "Stewart", "Nelson", "Kelly", "Cooper", "Camacho", "Best", "Williams", "Cabrera", "Floyd", "Hernandez", "Perez", "Patterson", "Jimenez", "Nelson", "Garza", "Love", "Brooks", "Barron", "Dickerson", "Myers", "Mathis", "Ward", "Kennedy", "Curry", "Johnston", "Smith", "Schmidt", "King", "Stanley", "Washington", "Howard", "Stevens", "Jensen", "Allen", "Pierce", "Scott", "Greene", "Moore", "Hays", "Vasquez", "Smith", "Patton", "Thomas", "Ruiz", "Wiley", "Gibbs", "Solis", "Green", "Carr", "Stephens", "Hall", "Lewis", "Hood", "Cook", "Reed", "Mora", ]


def get_fake_name():
    name = f'{random.choice(first_names)} {random.choice(last_names)}'
    return name


pickup_locations = ['London', 'Paris', 'Chicago', 'Boston', 'Seattle']


coordinates = {
    'London': {'LAT': 51.5007, 'LON': 0.1246},
    'Paris': {'LAT': 48.8584, 'LON': 2.2945},
    'Chicago': {'LAT': 41.8919, 'LON': 87.6051},
    'Boston': {'LAT': 42.3467, 'LON': 71.0972},
    'Seattle': {'LAT': 47.6205, 'LON': 122.3493}
}


def random_pickup_location():
    return random.choice(pickup_locations)


def random_destination_location(pickup):
    options = list(pickup_locations)
    options.remove(pickup)
    return random.choice(options)


def coords_to_string(location):
    lat = coordinates[location]['LAT']
    lon = coordinates[location]['LON']
    return f'{lat},{lon}'


def create_date_iso(previous_time, time_delta_seconds):
    if '.' not in previous_time:
        previous_time = previous_time + '.0'
    previous_time_dt = datetime.strptime(previous_time, '%Y-%m-%dT%H:%M:%S.%f')
    new_time = previous_time_dt + timedelta(seconds=time_delta_seconds)
    return new_time.isoformat()


def generate_event(date_iso):
    global repeat_customers
    pickup_location = random_pickup_location()
    destination_location = random_destination_location(pickup_location)
    order_event = {
        'customer_name': (random.choice(repeat_customers)[0] if chance(0.2) else get_fake_name()),
        'order_id': str(uuid4()),
        'pickup_coords': coords_to_string(pickup_location),
        'pickup_location': pickup_location,
        'destination_coords': coords_to_string(destination_location),
        'destination_location': destination_location,
        'event_ts': date_iso,
        'time_ordered': date_iso,
        'order_cost': costs[pickup_location][destination_location]
    }
    return order_event


def get_latest_parcel_order_time():
    params = {
        'token': 'p.eyJ1IjogIjMxYzFkMzllLTIzZjEtNDBmMC05ZjRhLTQ0NjliNThhNDE1MCIsICJpZCI6ICJlYTgxNDZjNi1mZjBlLTQ5MjktODBmOS1hNjhiNWNlNDUxNDcifQ.8siSrZxri7IlS4wdDMtPOiVYYLXMGXgxnVUSRcXhgMw'
    }
    url = f'https://api.tinybird.co/v0/pipes/get_latest_order_time.json'
    response = requests.get(url, params=params)
    if (response.status_code == 200):
        r = response.json()
        if (len(r['data']) > 0):
            return datetime.strptime(r['data'][0]['time'], '%Y-%m-%d %H:%M:%S.%f').isoformat()
    return None


def send_events(batch):
    nd_data = nd.dumps(batch)

    r = requests.post('https://api.tinybird.co/v0/events',
                      params={
                          'name': 'parcel_order_events',
                          'token': f'{TB_TOKEN}',
                      },
                      data=nd_data)
    if (r.status_code == 202):
        return True
    return False


batch = []
eps = 1000
last_sent_time = get_latest_parcel_order_time()
if (not last_sent_time):
    last_sent_time = (datetime.utcnow() - timedelta(days=7)).isoformat()

while True:
    wait = 1/eps
    event = generate_event(create_date_iso(last_sent_time, wait))
    last_sent_time = event['event_ts']
    batch.append(event)
    if (len(batch) == eps):
        send_events(batch)
        print(f'{datetime.utcnow().isoformat()} - batch sent: {len(batch)} rows')
        batch = []
    time.sleep(wait)
