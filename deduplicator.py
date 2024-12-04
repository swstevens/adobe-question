import json

class Processor:
    def __init__(self,filename):
        self.unique_ids = {}
        self.unique_emails = {}
        with open(filename, 'r') as input_file:
            self.input_data = json.load(input_file)['leads']
        self.num_elements = len(self.input_data)
        self.final_elements = [0 for _ in range(self.num_elements)]

    def remove_by_id(self,cur_id):
        if cur_id in self.unique_ids:
            other_email = self.input_data[self.unique_ids[cur_id]]['email']
            self.final_elements[self.unique_ids[cur_id]] = 0
            del self.unique_emails[other_email]
            del self.unique_ids[cur_id]

    def remove_by_email(self,cur_email):
        if cur_email in self.unique_emails:
            otherID = self.input_data[self.unique_emails[cur_email]]['_id']
            self.final_elements[self.unique_emails[cur_email]] = 0
            del self.unique_emails[cur_email]
            del self.unique_ids[otherID]
    
    def process_json(self):
        # check, in order, if there are any conflicts. If there are, remove any previous elements that conflicted.
        for i in range(self.num_elements):

            cur_email = self.input_data[i]['email']
            cur_id = self.input_data[i]['_id']
            if cur_email in self.unique_emails:
                self.remove_by_email(cur_email)
            if cur_id in self.unique_ids:
                self.remove_by_id(cur_id)
            self.unique_emails[cur_email] = i
            self.unique_ids[cur_id] = i
            self.final_elements[i] = 1
            print(self.final_elements)
        return

    def generate_file(self,filename):
        if not self.final_elements:
            self.process_json()
        
        # gather final json elements
        output =  []
        for i in range(self.num_elements):
            if self.final_elements[i]:
                output.append(self.input_data[i])

        # output elements to file
        with open(filename,'w+') as output_file:
            # json format here is somewhat hardcoded. assumption made due to singular example given
            json.dump({'leads':output},output_file,indent=0)
            


def main():
    processor = Processor('leads.json')
    processor.process_json()
    processor.generate_file('leads_out.json')

if __name__ == '__main__':
    main()