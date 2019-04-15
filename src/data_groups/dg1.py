import json

class DG1:
    """Data group 1
    Data:
        - family_name
        - name
        - date_of_birth
        - date_of_issue
        - date_of_expiry
        - issuing_country
        - issuing_authority
        - license_number
        - categories_of_vehicles
    """
    def __init__(self, data):
        if isinstance(data, str):
            self.load(data)
        else:
            self.family_name = data['family_name']
            self.name = data['name']
            self.date_of_birth = data['date_of_birth']
            self.date_of_issue = data['date_of_issue']
            self.date_of_expiry = data['date_of_expiry']
            self.issuing_country = data['issuing_country']
            self.issuing_authority = data['issuing_authority']
            self.license_number = data['license_number']
            self.categories_of_vehicles = data['categories_of_vehicles']

    def save(self, filename):
        """Dumps data group to file"""
        with open(filename, 'w+') as fp:
            payload = [
                self.family_name,
                self.name,
                self.date_of_birth,
                self.date_of_issue,
                self.date_of_expiry,
                self.issuing_country,
                self.issuing_authority,
                self.license_number,
                self.categories_of_vehicles
            ]
            # TODO: Cifrar?
            fp.write(json.dumps(payload))

    def load(self, filename):
        with open(filename, 'r') as fp:
            # TODO: Decifrar?
            [self.family_name,\
             self.name,\
             self.date_of_birth,\
             self.date_of_issue,\
             self.date_of_expiry,\
             self.issuing_country,\
             self.issuing_authority,\
             self.license_number,\
             self.categories_of_vehicles] = json.loads(fp.read())

    def __str__(self):
        return ';'.join([self.family_name,\
             self.name,\
             self.date_of_birth,\
             self.date_of_issue,\
             self.date_of_expiry,\
             self.issuing_country,\
             self.issuing_authority,\
             self.license_number,\
             self.categories_of_vehicles])

DATA = {'family_name': 'family_name', 'name': 'name', 'date_of_birth': '20191011', 'date_of_issue': '20191012', 'date_of_expiry': '20191013', 'issuing_country': 'aaa', 'issuing_authority': 'issuing_authority', 'license_number': 'license_number', 'categories_of_vehicles': 'C1;20000315;20100314;93;<=;8000'}
dg1 = DG1(DATA)
dg1.save('dg1.txt')
dg1.load('dg1.txt')

dg2 = DG1('dg1.txt')
print(dg2)
