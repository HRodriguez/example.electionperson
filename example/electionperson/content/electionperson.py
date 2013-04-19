"""Definition of the ElectionPerson content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-


from example.electionperson.config import PROJECTNAME

import logging
from sha import sha

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent

from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from zope.interface import implements, classImplements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.CMFCore.permissions import View, ModifyPortalContent, SetOwnPassword, SetOwnProperties
from Products.CMFCore.utils import getToolByName

from Products.membrane.at.interfaces import IUserAuthProvider, IPropertiesProvider, IGroupsProvider, IGroupAwareRolesProvider, IUserChanger

from example.electionperson.config import *
from example.electionperson.interfaces import IElectionPerson
from example.electionperson.interfaces import IElectionPersonModifiedEvent

from example.electionperson import electionpersonMessageFactory as _
ElectionPersonSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    StringField(
        name='firstName',
        widget=StringWidget(
            label=_(u"First Name", default=u"First Name"),
        ),
        required=True,

        searchable=True
    ),
    

    StringField(
        name='lastName',
        widget=StringWidget(
            label=_(u"Last Name", default=u"Last Name"),
        ),
        required=True,

        searchable=True
    ),
    
    StringField(
        name='email',
        user_property=True,
        widget=StringWidget(
            label=_(u"Email", default=u"Email"),

        ),

        searchable=True,
        validators=('isEmail',)
    ),
    
    StringField(
        name = 'gender',
        widget=SelectionWidget(
            label=_(u"Person Gender", default=u"Person Gender"),
        ),
        vocabulary=('Male', 'Female'),
        required=True,
    ),
        
    
    StringField(
        name='id',
        widget=StringWidget(
            label=_(u"Access Account ID", default=u"Access Account ID"),
            description=_(u"Example: abc123", default=u"Example: abc123"),
        ),
        required=True,
        user_property=True,


    ),
    
    ComputedField(
        name='title',
        widget=ComputedField._properties['widget'](
            label=_(u"Full Name", default=u"Full Name"),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),

        accessor="Title",
        user_property='fullname',
        searchable=True
    ),
    
  
    StringField('password',
        languageIndependent=True,
        required=False,
        mode='w',
        write_permission=SetOwnPassword,
        widget=PasswordWidget(
            label=_(u"Password", default=u"Password"),
            description=_(u"Password for this person (Leave blank if you don't want to change the password.)", default=u"Password for this person (Leave blank if you don't want to change the password.)"),

        ),

    ),


))

schemata.finalizeATCTSchema(ElectionPersonSchema, moveDiscussion=False)


class ElectionPersonModifiedEvent(object):
    """Event that happens when edits to a Person have been saved"""
    implements(IElectionPersonModifiedEvent)
    
    def __init__(self, context):
        self.context = context
        

class ElectionPerson(base.ATCTContent):
    """Election Person"""
    implements(IElectionPerson,
               IUserAuthProvider,
               IPropertiesProvider,
               IGroupsProvider,
               IGroupAwareRolesProvider,
               IAttributeAnnotatable,
               IUserChanger)

    meta_type = portal_type = "ElectionPerson"
    security = ClassSecurityInfo()
    ElectionPersonSchema.changeSchemataForField('description', 'metadata')
    schema = ElectionPersonSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    def __call__(self, *args, **kwargs):
        return self.getId()
    
   
    
    security.declareProtected(View, 'Title')
    def Title(self):
        """Return the Title as firstName middleName(when available) lastName, suffix(when available)"""
        try:
            # Get the fields using the accessors, so they're properly Unicode encoded.TOOLNAME
            # We also can't use the %s method of string concatentation for the same reason.
            # Is there another way to manage this?
            fn = self.getFirstName()
            ln = self.getLastName()
        except AttributeError:
            return u"new person" # YTF doesn't this display on the New Person page?  # Couldn't call superclass's Title() for some unknown reason
        
        t = fn +"-"+ ln
        
        return t
        
    security.declareProtected(SetOwnPassword, 'setPassword')
    def setPassword(self, value):
        """"""
        if value:
            annotations = IAnnotations(self)
            annotations[PASSWORD_KEY] = sha(value).digest()
    


atapi.registerType(ElectionPerson, PROJECTNAME)
