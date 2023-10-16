# Project Overview
## Team Members & Roles
| NAME | ROLE |
| --- | --- |
| Brian Kim | Full-Stack |
| Esther Wang | Back-End |
| Kaitlyn Chau | Front-End |
| Kevin Ng | Full-Stack |

## Tech Stack / Tools
- Front-end: React
- API server: flask and flask-restx
- OS: UNIX-like (MacOS, Linux, Windows Subsystem for Linux, etc.)
- Testing: pytest
- Database: MongoDB
- Build: make
- Lint: flake8
- CI/CD: GitHub Actions
- Cloud deployment: Heroku
- Project management: Notion & Kanban board on GitHub


# Potential Features
## Tasks
- Post Tasks
  - Tasks look like a blog which isn't simply like todos
  - Users can customize font size/weight/color
  - Can include lists (like bullet points) and tables
  - Can include an image
- Modify Task Attributes
  - Including update and delete

## Authentication
Authentication feature allows users to sign up for an account if they are a new user. If they are a returning user, they have the option to log in with their credientials, which will be used to autehnticate against our database for safe login.
- Returning User
  - Log in: User will provide username and password (encrypted) to authenicate against database
  - Log out: User will access 'Log Out' button, removing session ID to log out
- New User
  - Create Account Neccessary Credentials
    - First Name
    - Last Name
    - Date of Birth
    - Username 
    - Email Address 
    - Password
    - Reconfirm Password
## Follow Feature 
- As a user, I want to follow other users to view and interact with their blogs 
- As a user, I want to manage my followers to restrict who can view & interact w/ my blogs 
- As a user, I want to manage my followees to restrict whos blogs I want to view & interact 
## Group Feature 
- As a user, I want to form a group to view & edit blogs for a specific category 
- As a user, I want to add and remove group members to form the group

## Profile Summary
Detailed summary of profile and all things related to account
- Create custom profile (bio, introductions, public presence)
- Ability to modify profile information (i.e., username, name, channels)
- Overview of followers, following, and channels
- View past posts
- Create new posts


## Summary / Profile Statistics
Summary feature offers users a visualization of their activity and achievements within the application. This will provide summarized insights into their performance and progress. 
- Insights on user productivity
  - Weekly/ Monthly Activity: Line chart to visualize the number of tasks completed over time
  - Total Activity: Total number of activities completed
  - Time Spent: Cumulative time spent on activities
- Goal Setting
  - Opportunity to set goals to track based on statistics.

## Streaks
Streaks motivates users to maintain consistent engagement with the application, rewarding users for completing tasks on consecutive days.
- Streak is displayed publically on profile
- Notifications will be sent out to maintain streak
- Streaks completed by completing at least one task a day.

## Sketches
![Home Login Feed Wireframe](documentation/images/home_login_feed_wireframe_sketch.jpg)
![Profile Wireframe](documentation/images/profile_wireframe_sketch.jpg)
![Group Fellow Schema](documentation/images/group_follow_schema.jpg)
![Group Wireframe](documentation/images/group_wireframe_v1.jpg)
![Friend Wireframe](documentation/images/friend_wireframe_v1.jpg)
