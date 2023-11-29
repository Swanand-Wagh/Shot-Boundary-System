import { Pagination } from './Pagination';
import { ImageSkeleton } from './ImageSkeleton';
import React from 'react';
import { FrameList } from '../../constants/FrameList';

export const ImageGridDisplay = ({
  currentImg,
  setCurrentImage,
  currentPage,
  setCurrentPage,
  imagesList,
}) => {
  return (
    <div className="imageGallery__contentWraps imageGridDisplay">
      {currentImg !== -1 ? (
        <ul className="imageGalley__imageGridDisplay__imageGrid">
          {imagesList.slice((currentPage - 1) * 20, 20 * currentPage).map((item, idx) => {
            const frame = FrameList.find((frameItem) => frameItem.id === item.id);
            const frameDisplay = frame
              ? `Frames: ${frame.start} - ${frame.end}`
              : 'Frame not found';
            return (
              <li key={idx} className="imageGalley__imageGridDisplay__imageGrid__gridItems">
                <img
                  src={item.image}
                  alt={idx}
                  onClick={() => {
                    setCurrentImage(item.id);
                  }}
                />
                <span className="image__number">{item.id}</span>
                <small style={{ margin: '0 auto' }}>{frameDisplay}</small>
              </li>
            );
          })}
        </ul>
      ) : (
        <ImageSkeleton totalImages={87} currentPage={currentPage} />
      )}

      <Pagination currentPage={currentPage} setCurrentPage={setCurrentPage} />
    </div>
  );
};
