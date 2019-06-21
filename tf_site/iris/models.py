from django.db import models


class Iris(models.Model):
    class Meta:
        verbose_name_plural = 'Irises'

    # def __init__(self): 
    #     self.petal_length = 0
    #     self.petal_width = 0
    #     self.sepal_length = 0
    #     self.sepal_width = 0
    #     self.classification = 'test'

    id = models.AutoField(primary_key=True)
    # iris_id = models.IntegerField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    classification = models.TextField(max_length=20)

    def __repr__(self):
        # return "{}\nPL: {}\nPW: {}\nSL: {}\nSW: {}".format(classification, petal_length, petal_width, sepal_length, sepal_width)
        return "Classification: {}\n\tWidth\tLength\nPetal\t{}\t{}\nSepal\t{}\t{}".format(
            self.classification,
            self.petal_width,
            self.petal_length,
            self.sepal_width,
            self.sepal_length,
        )

    def __str__(self):
        return "{} --> SW: {} / SL: {} / PW: {} / PL: {}".format(
            self.classification, 
            self.sepal_width, 
            self.sepal_length,
            self.petal_width,
            self.petal_length,
        )

    def load(file):
        """
        Method to load a file to the model
        """
        print('Opening File: ', file)
        with open(file) as f:
            print('Processing File')
            for line in f:
                sl, sw, pl, pw, c = line.split(',')
                c = c.strip() # all but last record has invisible newline character that should be removed
                i = Iris(petal_length=pl, petal_width=pw, sepal_length=sl, sepal_width=sw, classification=c) 
                i.save()
            print('Done loading database')
        print("Closing file")
