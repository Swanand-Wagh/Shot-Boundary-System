import React, { useCallback, useEffect, useState } from 'react';
import { GrPowerReset } from 'react-icons/gr';
import { IoClose } from 'react-icons/io5';
import { RiImageAddFill } from 'react-icons/ri';
import { imageArray } from '../../constants/ImageList';

export const ImageFilters = ({
  currentImg,
  setCurrentImage,
  imagesList,
  setImagesList,
  setCurrentPage,
}) => {
  const [currentImgURL, setCurrentImageURL] = useState('');

  useEffect(() => {
    if (!imagesList) {
      setCurrentImageURL('');
      return;
    }

    const selectedImg = imagesList.find((img) => img.id === currentImg);
    setCurrentImageURL(!selectedImg ? '' : selectedImg.image);
  }, [currentImg]);

  return (
    <div className="imageGallery__contentWraps imageSelectDisplay">
      <div className="imageGallery__imageSelectDisplay__selectedImage">
        {currentImg !== -1 && (
          <div className="imageGallery__imageSelectDisplay__selectedImage__imageActionBtns">
            <button
              onClick={() => {
                setImagesList(imageArray);
                setCurrentPage(1);
                setCurrentImage(imageArray[0].id);
              }}
              className="imageGallery__imageSelectDisplay__selectedImage__imageActionBtns__resetBtn"
            >
              <GrPowerReset />
            </button>
            <button
              onClick={() => setCurrentImageURL('')}
              className="imageGallery__imageSelectDisplay__selectedImage__imageActionBtns__closeBtn"
            >
              <IoClose />
            </button>
          </div>
        )}

        <div
          style={{ background: currentImg !== -1 && currentImgURL ? 'transparent' : '#efedfc' }}
          className="imageGallery__imageSelectDisplay__selectedImage__imageWrap"
        >
          {currentImg !== -1 && currentImgURL ? (
            <React.Fragment>
              <img src={currentImgURL} alt="" />
              <span className="imageGallery__imageSelectDisplay__selectedImage__imageWrap__number">
                {currentImg}
              </span>
            </React.Fragment>
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
