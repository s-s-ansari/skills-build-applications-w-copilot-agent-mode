from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample users (super heroes)
        users = [
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team': 'Marvel'},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Black Widow']},
            {'name': 'DC', 'members': ['Superman', 'Batman', 'Wonder Woman']},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {'user': 'Superman', 'activity': 'Flying', 'duration': 120},
            {'user': 'Batman', 'activity': 'Martial Arts', 'duration': 90},
            {'user': 'Iron Man', 'activity': 'Weight Lifting', 'duration': 60},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 250},
            {'team': 'DC', 'points': 200},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Hero HIIT', 'description': 'High intensity interval training for heroes.'},
            {'name': 'Power Yoga', 'description': 'Yoga for strength and flexibility.'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
