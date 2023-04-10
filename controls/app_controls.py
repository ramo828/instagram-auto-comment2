from controls.database import Database
class Setting_controls:
    def __init__(self):
        self.db = Database()

    def checkSettingData(self, * args):
        for data in range(len(args)):
            if(not args[data]):
                print(f"bos {data}")
                continue
            else:
                print(f'Dolu: {data}')
                self.db.save_data_index(data, args[data])
            
