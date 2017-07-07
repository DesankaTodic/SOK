from django.db import models

class Attribute(models.Model):
    name=models.CharField(max_length=50)
    value=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Node(models.Model):
    code=models.CharField(max_length=120,default="")
    label=models.CharField(max_length=50)
    text=models.CharField(max_length=120,default="")
    #links=models.ManyToManyField(Link)#ka linkovi child cvorovima
    attributes=models.ManyToManyField(Attribute)#lista atributa

    def __str__(self):
        return self.label

class Link(models.Model):
    label=models.CharField(max_length=120)
    parent_node=models.ForeignKey(Node,on_delete=models.CASCADE,related_name='parent_node',default="")#ka kome cvoru je link
    child_node=models.ForeignKey(Node,on_delete=models.CASCADE,related_name='child_node',default="")#ka kome cvoru je link

    def __str__(self):
        return self.label


