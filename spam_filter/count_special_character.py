import re
from bs4 import BeautifulSoup

# RIGHT NOW I DONT EVEN KNOW IF WE SHOULD USE THIS

class AnalyseText():
    def result(self, filename):
        self.filename = filename
        self.file = open(self.filename, mode='r', encoding='UTF-8')
        self.email_body = self.file.read()
        self.clean_text = self.get_clean_text()
        
        points = self.overall_points()
        print(f'Points: {points}')
        
        self.file.close()
        
        if points >= -10:
            return 'OK'
        
        return 'SPAM'
    
    def overall_points(self):
        return self.count_safe_words() - self.count_money_mention() - self.count_special_characters()
    
    def get_clean_text(self):
        body_idx = -1
        body_idx = self.email_body.find("<BODY>")
        if body_idx != -1:
            self.email_body = self.email_body[body_idx:]

        soup = BeautifulSoup(self.email_body, "html.parser")
        
        # Extract the text content
        text = soup.get_text(separator="\n")
        
        # Remove leading/trailing whitespace and return
        return text.strip().lower()
    
    
    def count_special_characters(self):
        # this function counts the number of special characters in the email body
        special_characters = ['!', '?', '%', '*', '₤', '€', '$']
        count = 0
        
        for special in special_characters:
            count += self.clean_text.count(special)
        
        return count
    
    
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
        
        return count
    
    def count_safe_words(self):
        # this function counts the number of save words in the email body
        # idea about using nltk so it finds the synonyms of the words and counts them as well
        count = 0
        safe_words = [
            # Greetings and Salutations
            "Hello", "Hi", "Hey", "Greetings", "Dear", "Good morning", "Good afternoon", 
            "Good evening", "Welcome", "How are you", "Hope you're doing well",

            # Positive, Encouraging Terms
            "Congratulations", "Well done", "Great job", "Good work", "Nice", "Excellent",
            "Awesome", "Fantastic", "Superb", "Wonderful", "Impressive", "Proud", "Achieved", 
            "Success", "Victory", "Accomplished", "Amazing", "Pleased", "Delighted",

            # Thanks and Gratitude
            "Thank you", "Thanks", "Appreciate", "Grateful", "Thanks so much", "Much appreciated", 
            "Many thanks", "I appreciate it", "I’m thankful", "We are grateful",

            # Expressions of Support
            "Support", "Assistance", "Help", "Here to help", "Let me know", "Feel free to ask", 
            "We’re happy to assist", "Happy to help", "Don’t hesitate", "We’re at your service",

            # Positive Affirmations
            "Yes", "Sure", "Of course", "Absolutely", "Definitely", "Without a doubt", "No problem",
            "Sure thing", "All right", "Okay", "Certainly", "You’re welcome", "It’s my pleasure",
            
            # Polite Expressions
            "Please", "Kindly", "Would you mind", "Would you like", "Could you", "May I", 
            "If you don’t mind", "Be my guest", "I would appreciate", "I look forward to", 
            "Looking forward", "Thanks in advance"
        ]
        
        for word in safe_words:
            count += self.clean_text.count(word.lower())
        
        return count
    
if __name__ == "__main__":
    i = AnalyseText()
    i.result('C:/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/Spam_Filter_Project/spam_filter/test_files/hello.txt')