from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from social_media.decorators import verify_member
from social_media.models import Member, Friendship
from social_media.paginations import CustomPagination
from social_media.serializers import MemberSerializer, LoginSerializer


@api_view(['POST'])
def sign_up(request):
    """
    View for signing up the new user with fields - email, name and password
    """
    member_serializer = MemberSerializer(data=request.data)
    if member_serializer.is_valid():
        member_serializer.save()
        return Response(member_serializer.data)
    return Response({"message": "Member creation failed",
                     "errors": member_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def log_in(request):
    """
    View for logging in the user, required post data - email and password
    Returns:
        token: if the credentials are valid returns token
    """
    login_serializer = LoginSerializer(data=request.data)
    if login_serializer.is_valid():
        return Response(login_serializer.data)
    return Response({"message": "Can't Login",
                     "errors": login_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_users(request):
    """
    View for searching the members using email or name with parameter q
    Returns:
        at most 10 members would be returned based on the search
    """
    query = request.GET.get('q', '')
    member = Member.objects.filter(email__iexact=query)
    if member.exists():
        member_serializer = MemberSerializer(member.first())
    else:
        member_qs = Member.objects.filter(name__icontains=query).order_by('id')
        paginator = CustomPagination()
        paginated_items = paginator.paginate_queryset(member_qs, request)
        member_serializer = MemberSerializer(paginated_items, many=True)
    return Response(member_serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
@verify_member
def send_request(request, receiver):
    """
    View for sending request from one member to another
    """
    sender = request.user
    friendship = Friendship.objects.filter(from_member=sender, to_member=receiver)
    if friendship.exists():
        friendship_status = friendship.first().status
        if friendship_status == "Accepted":
            return Response({"message": f"Already friends with {receiver.name}"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": f"Friend request already exists with status - {friendship_status}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    Friendship.objects.create(from_member=sender, to_member=receiver)
    return Response({"message": f"Friend request sent to {receiver.name}"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@verify_member
def accept_request(request, sender):
    """
    View for accepting request from one member to another
    """
    receiver = request.user
    friendship = Friendship.objects.filter(from_member=sender, to_member=receiver)
    if not friendship.exists():
        return Response({"message": f"No friend request found from {sender.name}"},
                        status=status.HTTP_400_BAD_REQUEST)
    friendship = friendship.first()
    friendship_status = friendship.status
    if friendship_status in {"Accepted", "Rejected"}:
        return Response({"message": f"Friend request already {friendship_status}"},
                        status=status.HTTP_400_BAD_REQUEST)
    friendship.status = "Accepted"
    friendship.save()
    return Response({"message": f"Friend request accepted from {sender.name}"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@verify_member
def reject_request(request, sender):
    """
    View for rejecting request from one member to another
    """
    receiver = request.user
    friendship = Friendship.objects.filter(from_member=sender, to_member=receiver)
    if not friendship.exists():
        return Response({"message": f"No friend request found from {sender.name}"},
                        status=status.HTTP_400_BAD_REQUEST)
    friendship = friendship.first()
    friendship_status = friendship.status
    if friendship_status in {"Accepted", "Rejected"}:
        return Response({"message": f"Friend request already {friendship_status}"},
                        status=status.HTTP_400_BAD_REQUEST)
    friendship.status = "Rejected"
    friendship.save()
    return Response({"message": f"Friend request rejected from {sender.name}"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_friends(request):
    """
    View for listing the friends (accepted friends requests) of member
    """
    member = request.user
    members = Member.objects.filter(received_requests__from_member=member,
                                    received_requests__status="Accepted")
    member_serializer = MemberSerializer(members, many=True)
    return Response(member_serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    """
    View for listing pending requests of the member
    """
    member = request.user
    members = Member.objects.filter(sent_requests__to_member=member,
                                    sent_requests__status="Pending")
    member_serializer = MemberSerializer(members, many=True)
    return Response(member_serializer.data)

