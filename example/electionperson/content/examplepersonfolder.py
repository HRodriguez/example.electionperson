"""Definition of the ExamplePersonFolder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from example.electionperson.interfaces import IExamplePersonFolder
from example.electionperson.config import PROJECTNAME

ExamplePersonFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ExamplePersonFolderSchema['title'].storage = atapi.AnnotationStorage()
ExamplePersonFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ExamplePersonFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class ExamplePersonFolder(folder.ATFolder):
    """ExamplePersonFolder"""
    implements(IExamplePersonFolder)

    meta_type = "ExamplePersonFolder"
    schema = ExamplePersonFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ExamplePersonFolder, PROJECTNAME)
