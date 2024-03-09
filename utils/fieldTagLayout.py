from robotpy_apriltag import AprilTagField, loadAprilTagLayoutField


class FieldTagLayout():
    def __init__(self):
        self.fieldTags = loadAprilTagLayoutField(AprilTagField.k2024Crescendo)

    def lookup(self, tagId):
        return self.fieldTags.getTagPose(tagId)