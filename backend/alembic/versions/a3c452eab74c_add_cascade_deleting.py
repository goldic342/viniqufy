"""Add cascade deleting

Revision ID: a3c452eab74c
Revises: 85f5af2eca93
Create Date: 2024-09-15 14:00:25.385691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c452eab74c'
down_revision: Union[str, None] = '85f5af2eca93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'analysis', ['id'])
    op.drop_constraint('analysis_playlist_version_id_fkey', 'analysis', type_='foreignkey')
    op.create_foreign_key(None, 'analysis', 'playlist_version', ['playlist_version_id'], ['version_id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'artist', ['artist_id'])
    op.drop_constraint('artist_genre_association_artist_id_fkey', 'artist_genre_association', type_='foreignkey')
    op.drop_constraint('artist_genre_association_genre_id_fkey', 'artist_genre_association', type_='foreignkey')
    op.create_foreign_key(None, 'artist_genre_association', 'genre', ['genre_id'], ['name'], ondelete='CASCADE')
    op.create_foreign_key(None, 'artist_genre_association', 'artist', ['artist_id'], ['artist_id'], ondelete='CASCADE')
    op.drop_constraint('artist_track_association_artist_id_fkey', 'artist_track_association', type_='foreignkey')
    op.drop_constraint('artist_track_association_track_id_fkey', 'artist_track_association', type_='foreignkey')
    op.create_foreign_key(None, 'artist_track_association', 'track', ['track_id'], ['track_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'artist_track_association', 'artist', ['artist_id'], ['artist_id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'genre', ['name'])
    op.create_unique_constraint(None, 'playlist', ['playlist_id'])
    op.drop_constraint('playlist_track_association_playlist_version_id_fkey', 'playlist_track_association', type_='foreignkey')
    op.drop_constraint('playlist_track_association_track_id_fkey', 'playlist_track_association', type_='foreignkey')
    op.create_foreign_key(None, 'playlist_track_association', 'playlist_version', ['playlist_version_id'], ['version_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'playlist_track_association', 'track', ['track_id'], ['track_id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'playlist_version', ['version_id'])
    op.drop_constraint('playlist_version_playlist_id_fkey', 'playlist_version', type_='foreignkey')
    op.create_foreign_key(None, 'playlist_version', 'playlist', ['playlist_id'], ['playlist_id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'track', ['track_id'])
    op.create_unique_constraint(None, 'track_features', ['track_id'])
    op.drop_constraint('track_features_track_id_fkey', 'track_features', type_='foreignkey')
    op.create_foreign_key(None, 'track_features', 'track', ['track_id'], ['track_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'track_features', type_='foreignkey')
    op.create_foreign_key('track_features_track_id_fkey', 'track_features', 'track', ['track_id'], ['track_id'])
    op.drop_constraint(None, 'track_features', type_='unique')
    op.drop_constraint(None, 'track', type_='unique')
    op.drop_constraint(None, 'playlist_version', type_='foreignkey')
    op.create_foreign_key('playlist_version_playlist_id_fkey', 'playlist_version', 'playlist', ['playlist_id'], ['playlist_id'])
    op.drop_constraint(None, 'playlist_version', type_='unique')
    op.drop_constraint(None, 'playlist_track_association', type_='foreignkey')
    op.drop_constraint(None, 'playlist_track_association', type_='foreignkey')
    op.create_foreign_key('playlist_track_association_track_id_fkey', 'playlist_track_association', 'track', ['track_id'], ['track_id'])
    op.create_foreign_key('playlist_track_association_playlist_version_id_fkey', 'playlist_track_association', 'playlist_version', ['playlist_version_id'], ['version_id'])
    op.drop_constraint(None, 'playlist', type_='unique')
    op.drop_constraint(None, 'genre', type_='unique')
    op.drop_constraint(None, 'artist_track_association', type_='foreignkey')
    op.drop_constraint(None, 'artist_track_association', type_='foreignkey')
    op.create_foreign_key('artist_track_association_track_id_fkey', 'artist_track_association', 'track', ['track_id'], ['track_id'])
    op.create_foreign_key('artist_track_association_artist_id_fkey', 'artist_track_association', 'artist', ['artist_id'], ['artist_id'])
    op.drop_constraint(None, 'artist_genre_association', type_='foreignkey')
    op.drop_constraint(None, 'artist_genre_association', type_='foreignkey')
    op.create_foreign_key('artist_genre_association_genre_id_fkey', 'artist_genre_association', 'genre', ['genre_id'], ['name'])
    op.create_foreign_key('artist_genre_association_artist_id_fkey', 'artist_genre_association', 'artist', ['artist_id'], ['artist_id'])
    op.drop_constraint(None, 'artist', type_='unique')
    op.drop_constraint(None, 'analysis', type_='foreignkey')
    op.create_foreign_key('analysis_playlist_version_id_fkey', 'analysis', 'playlist_version', ['playlist_version_id'], ['version_id'])
    op.drop_constraint(None, 'analysis', type_='unique')
    # ### end Alembic commands ###
