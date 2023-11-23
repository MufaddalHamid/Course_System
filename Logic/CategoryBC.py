import uuid
from datetime import date
from sqlalchemy import or_, and_
from Datamodel.Category import Category
from Datamodel.Category_Basket import Category_Basket
from Logic.AppHelper import ActiveSession


class CategoryBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_Category()

    def load_Category(self):
        try:
            if self.SysId is not None:
                print('SysID is not null')
                self.category = ActiveSession.Session.query(
                    Category).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized empty Category')
                self.category = Category()
        except Exception as e:
            print(f"Error loading Category data: {str(e)}")
            self.category = None

    def create_Category(self, new_category):
        try:
            print('Trying to create')
            self.category = Category(**new_category)
            category_exists = ActiveSession.Session.query(Category).filter_by(Category_Name=self.category.Category_Name).first()
            if category_exists:
                raise ValueError(
                    f'Category already existed | User already Created {category_exists.Category_Name}!!')
            else:
                self.category.SysId = str(uuid.uuid4())
                ActiveSession.Session.add(self.category)
                ActiveSession.Session.commit()
                new_category['message'] = 'Category created successfully'
                new_category['SysId'] = str(self.category.SysId)
                new_category['Code'] = 201
                return new_category
        except Exception as e:
            ActiveSession.Session.rollback()
            new_category['message'] = str(e)
            new_category['Code'] = 500
            return new_category

    def get_categories(self):
        try:
            if self.SysId is None:
                results = ActiveSession.Session.query(Category).all()
                return results
            else:
                if self.category:
                    return self.category
                else:
                    return {"error": "Category not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_Category(self, new_data):
        try:
            if self.category is not None:
                for key, value in new_data.items():
                    setattr(self.category, key, value)
                ActiveSession.Session.commit()
                return {"message": "Category updated successfully ", "Code": 201}
            else:
                return {"message": "Category not found", 'Code': 404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), 'Code': 500}

    def delete_Category(self):
        try:
            # Make sure self.category is loaded or associated with the active session
            # Now you should be able to delete it
            ActiveSession.Session.delete(self.category)
            ActiveSession.Session.commit()
            return {"message": "Category deleted successfully", "Code": 201}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e), "Code": 500}
