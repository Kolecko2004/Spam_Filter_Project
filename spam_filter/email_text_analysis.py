import re
from bs4 import BeautifulSoup
import numpy as np

# RIGHT NOW I DONT EVEN KNOW IF WE SHOULD USE THIS

class AnalyseText():
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, mode='r', encoding='UTF-8')
        self.email_body = self.file.read()
        self.clean_text = self.get_clean_text()
    
    def get_clean_text(self):
        body_idx = -1
        body_idx = self.email_body.find("<BODY>")
        if body_idx != -1:
            self.email_body = self.email_body[body_idx:]

        soup = BeautifulSoup(self.email_body, "html.parser")
        
        # Extract the text content
        text = soup.get_text(separator="\n")
        
        return text.strip().lower()
    
    def count_special_characters(self):
        # this function counts the number of special characters in the email body
        special_characters = ['!', '%', '*', '₤', '€', '$']
        count = 1
        
        for special in special_characters:
            count += self.clean_text.count(special)
        
        score = 12 - count
        if score > 10:
            return 10
        return max(-10, score)
        
    def count_money_mention(self):
        # this function counts the number of money related words in the email body
        count = 0
        money_related_words = [
            # Monetary Terms
            "Price", "Cost", "Value", "Payment", "Amount", "Charge", "Deposit", 
            "Withdrawal", "Loan", "Credit", "Cash", "Check", "Bank", "Savings", 
            "Wallet", "Account",

            # Marketing and Promotional Terms
            "Free", "Discount", "Sale", "Offer", "Save", "Deal", "Bonus", "Extra", 
            "Giveaway", "Limited", "Exclusive",

            # Winning and Rewards
            "Win", "Jackpot", "Prize", "Reward", "Earn", "Gift", "Big", "Fortune", 
            "Gain", "Treasure",

            # Action-Oriented Words
            "Buy", "Pay", "Get", "Purchase", "Subscribe", "Claim", "Redeem", 
            "Transfer", "Add",

            # Adjectives and Descriptors
            "Easy", "Fast", "Quick", "Huge", "Massive", "Big", "Unlimited", 
            "Guaranteed",

            # Risky or Suspicious Words
            "Urgent", "Immediate", "Now", "Today", "Risk-free", "No-obligation", 
            "100%", "Secure"
        ]
        
        for word in money_related_words:
            count += self.clean_text.count(word.lower())
        
        score = 15 - count
        if score > 10:
            return 10
        return max(-10, score)
    
if __name__ == "__main__":
    i = AnalyseText('C:/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/Spam_Filter_Project/spam_filter/test_files/hello.txt')
    print(i.count_special_characters())
    print(i.count_money_mention())