# python
import json
import os
from MoneyTracker.MONEY_TRACK.models import Transaction


class JsonFileFactory:
    def write_data(self, arr_data, filename):
        try:
            json_string = json.dumps(
                [item.to_dict() if hasattr(item, "to_dict") else item for item in arr_data],
                indent=4,
                ensure_ascii=False
            )
            with open(filename, 'w', encoding='utf-8') as json_file:
                json_file.write(json_string)
        except Exception as e:
            print(f"Error writing to JSON file: {e}")

    def read_data(self, filename, ClassName):
        if not os.path.isfile(filename):
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                arr_data = json.loads(
                    file.read(),
                    object_hook=lambda d: self.map_keys_to_class(d, ClassName)
                )
            return arr_data
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return []

    def map_keys_to_class(self, dict_obj, ClassName):
        if ClassName == Transaction:
            return ClassName(
                TransactionNo=dict_obj.get("TransactionNo", dict_obj.get("No.")),
                TransactionDate=dict_obj.get("TransactionDate", dict_obj.get("Date")),
                Amount=dict_obj.get("Amount"),
                Category=dict_obj.get("Category")
            )
        return ClassName(**dict_obj)