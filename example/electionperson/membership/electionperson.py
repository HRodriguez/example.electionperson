from Acquisition import aq_inner, aq_parent
from zope.interface import implements
from zope.component import adapts
from sha import sha

from Products.CMFCore.utils import getToolByName

from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations

from Products.membrane.interfaces import IMembraneUserObject
from Products.membrane.at.interfaces import IUserAuthentication
from Products.membrane.at.interfaces import IUserRoles
from Products.membrane.interfaces import IMembraneUserManagement
from example.electionperson.interfaces.electionperson import IElectionPerson
from example.electionperson.config import PASSWORD_KEY


class UserRelated(object):
    """Provide a user id for persons.
    
    The user id will simply be the id of the member object. This overrides the
    use of UIDs
    """
    implements(IMembraneUserObject)
    adapts(IElectionPerson)

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        return self.context.getId()    

    def getUserName(self):
        return self.context.getId()

class UserAuthentication(object):
    """Provide authentication against persons.
    
    configurable to use internally-stored passwords, or to pass on verification to
    another PAS plugin (perhaps a SSO like apachepas or pubcookiepas)
    """
    implements(IUserAuthentication)
    adapts(IElectionPerson)
    
    def __init__(self, context):
        self.context = context

    def getUserName(self):
        return self.context.getId()
    
    def verifyCredentials(self, credentials):
        """Authenticate against the password stored via attribute on this person,
        or pass authentication on to the next PAS plugin
        """

        login = credentials.get('login', None)
        password = credentials.get('password', None)
         
        if login is None or password is None:
            return False
            
        digest = sha(password).digest()
        annotations = IAnnotations(self.context)
        passwordDigest = annotations.get(PASSWORD_KEY, None)
        return (login == self.getUserName() and digest == passwordDigest)

         
class UserRoles(object):
    """Provide roles for person users.
    
    Roles may be set (by sufficiently privileged users) on the user object.
    """
    implements(IUserRoles)
    adapts(IElectionPerson)
    
    def __init__(self, context):
        self.context = context
        
    def getRoles(self):
        # return self.context.getRoles()
        return ()

class UserManagement(object):
    """Provides methods for adding deleting and changing users

    This is an implementation of IUserManagement from PlonePAS
    """
    implements(IMembraneUserManagement)
    adapts(IElectionPerson)

    def __init__(self, context):
        self.context = context

    def doAddUser(self, login, password):
        """This can't be done unless we have a canonical place to store users
        some implementations may wish to define one and implement this.
        """
        raise NotImplementedError

    def doChangeUser(self, login, password, **kw):
        self.context.setPassword(password)
        if kw:
            self.context.edit(**kw)

    def doDeleteUser(self, login):
        parent = aq_parent(aq_inner(self.context))
        parent.manage_delObjects([self.context.getId()])
