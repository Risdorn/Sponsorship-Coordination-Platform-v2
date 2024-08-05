from faker import Faker
from components.models import Ad_request, Campaign
from components.extensions import bcrypt, industries, categories, datastore

user_ids = []
user_id = 2
campaign_id=1
# Initialize Faker for generating random data
fake = Faker()

# Function to create sample users
def create_sample_sponsors(n):
    global user_id
    global user_ids
    user_ids = []
    users = []
    for _ in range(n):
        email = fake.email()
        password = fake.password(special_chars=True, digits=True, upper_case=True, lower_case=True)
        print(f"Sponsor email: {email}, password: {password}")
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = datastore.create_user(
            roles=['Sponsor'],
            name=fake.name(),
            email=email,
            password=password,
            industry=fake.random_element(elements=industries),
            created_on=fake.date_this_year(before_today=True),
            active=True
        )
        users.append(user)
        user_ids.append(user_id)
        user_id += 1
    return users

def create_sample_influencers(n):
    users = []
    global user_id
    global user_ids
    user_ids = []
    for _ in range(n):
        email = fake.email()
        password = fake.password(special_chars=True, digits=True, upper_case=True, lower_case=True)
        print(f"Influencer email: {email}, password: {password}")
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = datastore.create_user(
            roles=['Influencer'],
            name=fake.name(),
            email=email,
            password=password,
            category=fake.random_element(elements=categories),
            reach=fake.random_number(digits=5),
            created_on=fake.date_this_year(before_today=True),
            active=True
        )
        users.append(user)
        users.append(user)
        user_ids.append(user_id)
        user_id += 1
    return users

# Function to create sample campaigns
def create_sample_campaigns_public(n):
    global user_ids
    global campaign_id
    campaigns = []
    for _ in range(n):
        sponsor = fake.random_element(user_ids)
        budget = fake.random_number(digits=5)
        campaign = Campaign(
            id=campaign_id,
            sponsor_id=sponsor,
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            goals=fake.text(max_nb_chars=200),
            category=fake.random_element(elements=categories),
            budget=budget,
            remaining=budget,
            visibility='Public',
            start_date=fake.date_this_year(before_today=True),
            end_date=fake.date_this_year(after_today=True),
            created_on=fake.date_this_year(before_today=True)
        )
        campaign_id+=1
        campaigns.append(campaign)
    return campaigns

def create_sample_campaigns_private(n):
    global user_ids
    global campaign_id
    campaigns = []
    for _ in range(n):
        sponsor = fake.random_element(user_ids)
        budget = fake.random_number(digits=5)
        campaign = Campaign(
            id=campaign_id,
            sponsor_id=sponsor,
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            goals=fake.text(max_nb_chars=200),
            category=fake.random_element(elements=categories),
            budget=budget,
            remaining=budget,
            visibility='Private',
            start_date=fake.date_this_year(before_today=True),
            end_date=fake.date_this_year(after_today=True),
            created_on=fake.date_this_year(before_today=True)
        )
        campaign_id+=1
        campaigns.append(campaign)
    return campaigns

# Function to create sample ad requests
def create_sample_ad_requests(campaigns, n):
    global user_ids
    ad_requests = []
    ad_request_id=1
    for _ in range(n):
        influencer = fake.random_element(user_ids)
        campaign = fake.random_element(campaigns)
        ad_request = Ad_request(
            id=ad_request_id,
            influencer_id=influencer,
            campaign_id=campaign.id,
            messages=fake.text(max_nb_chars=200),
            requirements=fake.text(max_nb_chars=200),
            payment_amount=fake.random_number(digits=4),
            status='Pending',
            negotiate=fake.boolean(),
            created_on=fake.date_this_year(before_today=True)
        )
        ad_request_id+=1
        ad_requests.append(ad_request)
    return ad_requests

def generate_sample_data(db):
    # Generate sample data
    create_sample_sponsors(3)
    public_campaigns = create_sample_campaigns_public(10)
    private_campaigns = create_sample_campaigns_private(10)
    create_sample_influencers(3)
    ad_requests = create_sample_ad_requests(public_campaigns, 30)

    # Add data to session and commit
    db.session.add_all(public_campaigns)
    db.session.add_all(private_campaigns)
    db.session.add_all(ad_requests)
    create_sample_sponsors(12)
    public_campaigns = create_sample_campaigns_public(100)
    private_campaigns = create_sample_campaigns_private(100)
    create_sample_influencers(12)
    db.session.add_all(public_campaigns)
    db.session.add_all(private_campaigns)

    print("Sample data generated and committed to the database!")
