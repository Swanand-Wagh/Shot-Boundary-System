import React, { useEffect, useState } from 'react';
import { RiImageAddFill } from 'react-icons/ri';

export const ImageFilters = ({ currentImg, imagesList }) => {
  const [currentImgURL, setCurrentImageURL] = useState('');

  useEffect(() => {
    if (!imagesList) {
      setCurrentImageURL('');
      return;
    }

    const selectedImg = imagesList.find((img) => img.id === currentImg);
    setCurrentImageURL(selectedImg ? selectedImg.image : '');
  }, [currentImg, imagesList]);

  return (
    <div className="imageGallery__contentWraps imageSelectDisplay">
      <div className="imageGallery__imageSelectDisplay__selectedImage">
        <div
          style={{ background: currentImg !== -1 && currentImgURL ? 'transparent' : '#efedfc' }}
          className="imageGallery__imageSelectDisplay__selectedImage__imageWrap"
        >
          {currentImg !== -1 && currentImgURL ? (
            <video controls muted src={`/videos/${currentImg}.mp4`}></video>
          ) : (
            <div className="imageGallery__imageSelectDisplay__selectedImage__noImage">
              <span className="imageGallery__imageSelectDisplay__selectedImage__noImage__noImgIcon">
                <RiImageAddFill />
              </span>
              <p className="imageGallery__imageSelectDisplay__selectedImage__noImage__noImageMsg">
                Select a Frame to Play the Video
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageFilters;
