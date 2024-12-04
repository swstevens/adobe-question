import json

class Processor:
    def __init__(self,filename):
        self.unique_ids = {}
        self.unique_emails = {}
        with open(filename, 'r') as input_file:
            self.input_data = json.load(input_file)['leads']
        self.num_elements = len(self.input_data)
        self.current_elements = [0 for _ in range(self.num_elements)]

    def remove_by_id(self,curID):
        if curID in self.unique_ids:
            self.current_elements[self.unique_ids[curID]] = 0
            del self.unique_ids[curID]

    def remove_by_email(self,curEmail):
        if curEmail in self.unique_emails:
            self.current_elements[self.unique_emails[curEmail]] = 0
            del self.unique_emails[curEmail]
    
    def process_json(self):
        for i in range(self.num_elements):
            curEmail = self.input_data[i]['email']
            curID = self.input_data[i]['_id']
            if curEmail in self.unique_emails:
                self.remove_by_email(curEmail)
            if curID in self.unique_ids:
                self.remove_by_id(curID)
            self.unique_emails[curEmail] = i
            self.unique_ids[curID] = i
            self.current_elements[i] = 1
        
            print(self.current_elements)
        return

    def generate_file(self,filename):
        if not filename:
            return
        if not self.current_elements:
            self.process_json()
        output =  []
        for i in range(self.num_elements):
            if self.current_elements[i]:
                output.append(self.input_data[i])
        with open(filename,'w+') as output_file:
            json.dump({'leads':output},output_file,indent=0)
            


def main():
    processor = Processor('leads.json')
    processor.process_json()
    processor.generate_file('leads_out.json')

if __name__ == '__main__':
    main()