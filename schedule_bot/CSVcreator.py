import pandas as pd


df = pd.DataFrame(data=[['9.00-12.15', '-', '-', "Unity", '-',
                         "Project Monitoring", "Agile", '-'],
                        ['12.30-15.30', '-', '-', '-', '-', '-', 'Python', '-'],
                        ['18.15-21.30', 'Data analysis', 'AI',
                         'English', 'Software engineering', '-', '-', '-']],
                  columns=['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', "Sunday"],
                  )
df.to_csv('schedule.csv', index=False)