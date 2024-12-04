from deduplicator import Processor
import unittest
import json

class TestJSONProcessing(unittest.TestCase):
    def test_json_processing(self):        
        files = [('leads','tests/expected_leads.json'),
                    ('id_then_new_email','tests/id_then_new_email_expected.json'),
                    ('id_then_old_email','tests/id_then_old_email_expected.json'),    
                    ('double_conflict','tests/double_conflict_expected.json'),    
                ]        
        # Run your processing function
        for file, expected in files:
            print()
            print(f"running test for {file}")
            in_file = f"tests/{file}.json"
            out_file = f"tests/{file}_out.json"
            processor = Processor(in_file)
            processor.process_json()
            processor.generate_file(out_file)
            with open(out_file, 'r') as output_file:
                actual_output = json.load(output_file) 
            # Load expected output JSON
            with open(expected, 'r') as expected_file:
                expected_output = json.load(expected_file) 
            
            # Compare outputs using assertEqual
            self.assertEqual(actual_output, expected_output, 
                            "Function output does not match expected output")
            
if __name__ == '__main__':
    unittest.main()