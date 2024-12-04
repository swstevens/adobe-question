from deduplicator import Processor
import unittest
import json

class TestJSONProcessing(unittest.TestCase):
    def test_json_processing(self):        
        files = [('leads','expected_leads.json')]        
        # Run your processing function
        for file, expected in files:
            in_file = f"{file}.json"
            out_file = f"{file}_out.json"
            processor = Processor(in_file)
            # processor.process_json()
            processor.generate_file(out_file)
            with open(out_file, 'r') as output_file:
                actual_output = json.load(output_file) 
            # Load expected output JSON
            with open(expected, 'r') as expected_file:
                expected_output = json.load(expected_file) 
            
            # Compare outputs using assertEqual
            self.assertEqual(actual_output, expected_output, 
                            "Function output does not match expected output")
