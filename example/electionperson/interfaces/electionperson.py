from zope.interface import Interface, Attribute
# -*- Additional Imports Here -*-
from zope import schema

class IElectionPerson(Interface):
    """Election Person"""

    # -*- schema definition goes here -*-
    
class IElectionPersonMembership(Interface):
    """An person, which is also a user.
    """
    
    id = schema.TextLine(title=u'Identifier',
                         description=u'An identifier for the employee',
                         required=True,
                         readonly=True)
    
    fullname = schema.TextLine(title=u'Full name',
                               description=u"The employee's full name for display purposes",
                               required=True,
                               readonly=True)
                               
class IElectionPersonModifiedEvent(Interface):
    """An event fired when a person object is saved.
    """
    
    context = Attribute("The content object that was saved.")
    
class IElectionPersonAddable(Interface):
    """A content type to be set as an addable_type within a Person."""
