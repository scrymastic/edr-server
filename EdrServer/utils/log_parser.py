

from pathlib import Path
from evtx import PyEvtxParser
from typing import Dict, List
import json



class LogParser:
    """
    A class that implements a log parser for parsing Windows Event Viewer log files.
    """
    def __init__(self):
        pass


    def parse_log_file(self, log_path: Path) -> List[Dict]:
        try:
            log_path = str(log_path)    # PyEvtxParser only accepts string path
            parser = PyEvtxParser(log_path)
            events = []
            print(f"log_path: {log_path}")
            for record in parser.records_json():
                event = self.parse_record(record)
                if event is not None:
                    events.append(event)
            return events
        except Exception as e:
            print(f"Error: {e}")
            return []


    def parse_record(self, record: Dict) -> Dict:
        """
        Parse a single record from the log file.
        """
        if record is None:
            return None
        data = json.loads(record["data"]).get("Event", {})
        system = data.get("System", {})
        system['Execution'] = system['Execution']['#attributes']
        system['Provider'] = system['Provider']['#attributes']
        system['Security'] = system['Security']['#attributes']
        system['TimeCreated'] = system['TimeCreated']['#attributes']
        
        if correlation := system.get('Correlation'):
            system['Correlation'] = system['Correlation']['#attributes']
        else:
            system['Correlation'] = {}
        
        event_data = data.get("EventData", {})
        event = {"System": system, "EventData": event_data}
        # event = EventMethod.assign_event_universal_id(event)
        return event

        

if __name__ == "__main__":
    pass

