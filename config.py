from dotenv import load_dotenv
import os

load_dotenv()

SESSION_COOKIE = os.getenv("LEETCODE_SESSION")
USERNAME = os.getenv("LEETCODE_USERNAME")

#This is the single place in your project that reads credentials. 
# Every other file imports from here — nothing reads .env directly.