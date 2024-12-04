import sys
import json
from datetime import datetime

class Logger:
    def __init__(self,log_file='tests/log.txt'):
        self.log_file = log_file
    def print(self, message):
        print(message)
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
            f.write(timestamp + message + "\n")
class Processor:
    def __init__(self,filename,logfile='tests/log.txt'):
        self.unique_ids = {}
        self.unique_emails = {}
        with open(filename, 'r') as input_file:
            self.input_data = json.load(input_file)['leads']
        self.num_elements = len(self.input_data)
        self.final_elements = [0 for _ in range(self.num_elements)]
        self.logger = Logger(logfile)
        self.logger.print(f"Starting Process. Initial Data: {self.input_data}")

    def remove_by_id(self,cur_id):
        if cur_id in self.unique_ids:
            other_email = self.input_data[self.unique_ids[cur_id]]['email']
            self.final_elements[self.unique_ids[cur_id]] = 0
            self.logger.print(f"Element {self.unique_ids[cur_id]} removed: ID Conflict on {cur_id}")

            del self.unique_emails[other_email]
            del self.unique_ids[cur_id]

    def remove_by_email(self,cur_email):
        if cur_email in self.unique_emails:
            otherID = self.input_data[self.unique_emails[cur_email]]['_id']
            self.final_elements[self.unique_emails[cur_email]] = 0
            self.logger.print(f"Element {self.unique_emails[cur_email]} removed: Email Conflict on {cur_email}")

            del self.unique_emails[cur_email]
            del self.unique_ids[otherID]
    
    def process_json(self):
        self.logger.print("Starting Processing")
        
        # check, in order, if there are any conflicts. If there are, remove any previous elements that conflicted.
        for i in range(self.num_elements):
            cur_email = self.input_data[i]['email']
            cur_id = self.input_data[i]['_id']
            self.logger.print(f"Processing Element {i} | ID: {cur_id} | EMAIL: {cur_email}")

            if cur_email in self.unique_emails:
                self.remove_by_email(cur_email)
            if cur_id in self.unique_ids:
                self.remove_by_id(cur_id)
            self.unique_emails[cur_email] = i
            self.unique_ids[cur_id] = i
            self.final_elements[i] = 1
        return

    def generate_file(self,filename='out.json'):
        self.logger.print("Parsing JSON Content")
        if not self.final_elements:
            self.process_json()
        
        # gather final json elements
        output =  []
        for i in range(self.num_elements):
            if self.final_elements[i]:
                output.append(self.input_data[i])
        self.logger.print(f"Final Data: {output}")
        self.logger.print(f"Starting Write to File")
        # output elements to file
        with open(filename,'w+') as output_file:
            # json format here is somewhat hardcoded. assumption made due to singular example given
            json.dump({'leads':output},output_file,indent=0)
        self.logger.print("Process Complete!\n")
            


def main():
    if len(sys.argv) <= 1:
        print("Must specify in-file. Out File Optional.")
        return

    processor = Processor(sys.argv[1])
    processor.process_json()
    if len(sys.argv) >= 3:
        processor.generate_file(sys.argv[2])
    else:
        processor.generate_file()

if __name__ == '__main__':
    main()