from abaqus import *
from abaqusConstants import *
import random
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
cliCommand("""session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry= COORDINATE)""")
chang,kuan,gao,cheng = getInputs((('please enter the value of length :',''),
                                  ('please enter the value of width :',''),
                                  ('please enter the value of heigth :',''),
                                  ('please enter the value of layer :','')))

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(float(chang), float(kuan)))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s, depth=float(gao))
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

heigth_one_lay = float(gao)/int(cheng)

for i in range(int(cheng)-1):
    p = mdb.models['Model-1'].parts['Part-1']
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=heigth_one_lay + i*heigth_one_lay)
    

p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
point_value = heigth_one_lay/2.0
for j in range(int(cheng)-1):
    pickedCells = c.findAt(((0, 0, point_value+j*heigth_one_lay), ))
    d1 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d1[j+2], cells=pickedCells)


for k in range(int(cheng)):
    mdb.models['Model-1'].Material(name='Material-'+ str(k+1))
    mdb.models['Model-1'].materials['Material-'+str(k+1)].Elastic(table=((2e5, 0.3), 
        ))
    mdb.models['Model-1'].materials['Material-'+str(k+1)].Plastic(table=((235.0, 0.0), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-'+str(k+1), 
        material='Material-'+str(k+1), thickness=None)
      

p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
point_value = heigth_one_lay/2.0
for j in range(int(cheng)):
    cells = c.findAt(((0, 0, point_value+j*heigth_one_lay), ))
    region = p.Set(cells=cells, name='Set-'+str(j+1))
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-'+str(j+1), offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)


session.viewports['Viewport: 1'].enableMultipleColors()
session.viewports['Viewport: 1'].setColor(initialColor='#BDBDBD')
cmap=session.viewports['Viewport: 1'].colorMappings['Material']
session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
session.viewports['Viewport: 1'].disableMultipleColors()

print 'done'