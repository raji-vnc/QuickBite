from delivery.models import Rider,DeliveryAssignment


def auto_assign_rider(order):
    rider=Rider.objects.filter(is_available=True).first()
    if rider:
        DeliveryAssignment.objects.create(
            rider=rider,
            order=order
        )
        rider.is_available=False
        rider.save()

        return rider
    return None