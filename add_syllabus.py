from app import app, db, Syllabus, SUBJECT_CODES, DEPARTMENTS, SEMESTERS, UNITS

def add_all_subjects():
    with app.app_context():
        # First, let's clear existing entries to avoid duplicates
        db.session.query(Syllabus).delete()
        db.session.commit()
        
        # Now add all subjects for each department and semester
        for department in DEPARTMENTS.keys():
            for semester in SEMESTERS:
                for subject in SUBJECT_CODES[department]:
                    syllabus = Syllabus(
                        department=department,
                        semester=semester,
                        subject=subject,
                        units=','.join(UNITS)
                    )
                    db.session.add(syllabus)
                    print(f'Adding {subject} for {department} - {semester}')
        
        db.session.commit()
        print("All subjects have been added successfully!")

if __name__ == '__main__':
    add_all_subjects() 