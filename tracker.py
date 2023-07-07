import math

class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

    def update(self, objects_rect):
        objects_bbs_ids = []

        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 50:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            if same_object_detected is False:
                self.id_count += 1
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])

        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            abcd, efgh, ijkl, mnop, object_id = obj_bb_id
            if object_id in self.center_points:
                # center = self.center_points[object_id]
                new_center_points[object_id] = self.center_points[object_id]

        self.center_points = new_center_points.copy()
        return objects_bbs_ids


    def register(self, cx, cy):
        # Register a new object with its center point
        self.center_points[self.id_count] = (cx, cy)
        self.id_count += 1

    def unregister(self, object_id):
        # Unregister an object with the given ID
        if object_id in self.center_points:
            del self.center_points[object_id]